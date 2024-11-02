from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping, NotRequired, TypedDict

import networkx as nx
import serde.csv
import serde.json
from joblib import Parallel, delayed
from libactor.cache import cache
from tqdm import tqdm

from statickg.helper import FileSqliteBackend, logger_helper
from statickg.models.etl import ETLOutput
from statickg.models.file_and_path import (
    FormatOutputPath,
    FormatOutputPathModel,
    InputFile,
    RelPath,
)
from statickg.models.repository import Repository
from statickg.services.interface import BaseFileService, BaseService

"""
Create a dedup group sites that are the same as each other.

This service works in two steps:

1. For each file, it produces a mapping from each site to a local dedup group.
2. Then, we map each local dedup to a final dedup site. Hopefully this graph is much smaller and much sparse.
3. Then, we generate same-as and dedup group.

"""


class SameAsServiceConstructArgs(TypedDict):
    verbose: NotRequired[int]
    parallel: NotRequired[bool]


class SameAsServiceInvokeArgs(TypedDict):
    input: RelPath | list[RelPath]
    output: RelPath | FormatOutputPath
    optional: NotRequired[bool]
    compute_missing_file_key: NotRequired[bool]


class SameAsService(BaseFileService[SameAsServiceInvokeArgs]):
    def __init__(
        self,
        name: str,
        workdir: Path,
        args: SameAsServiceConstructArgs,
        services: Mapping[str, BaseService],
    ):
        super().__init__(name, workdir, args, services)
        self.verbose = args.get("verbose", 1)
        self.parallel = args.get("parallel", True)
        self.parallel_executor = Parallel(n_jobs=-1, return_as="generator_unordered")

    def forward(
        self, repo: Repository, args: SameAsServiceInvokeArgs, tracker: ETLOutput
    ):
        infiles = self.list_files(
            repo,
            args["input"],
            unique_filepath=True,
            optional=args.get("optional", False),
            compute_missing_file_key=args.get("compute_missing_file_key", True),
        )
        outfmt = FormatOutputPathModel.init(args["output"])

        jobs = []
        for infile in infiles:
            outfile = outfmt.get_outfile(infile.path)
            outfile.parent.mkdir(parents=True, exist_ok=True)
            group_prefix = outfile.parent / outfile.stem
            jobs.append((group_prefix, infile, outfile))

        readable_ptns = self.get_readable_patterns(args["input"])

        if self.parallel:
            it: Iterable = self.parallel_executor(
                delayed(step1_exec)(self.workdir, group_prefix, infile, outfile)
                for group_prefix, infile, outfile in jobs
            )
        else:
            it: Iterable = (
                step1_exec(self.workdir, group_prefix, infile, outfile)
                for group_prefix, infile, outfile in jobs
            )

        outfiles = set()
        for outfile in tqdm(
            it, desc=f"Generating same-as for {readable_ptns}", disable=self.verbose < 1
        ):
            outfiles.add(outfile.relative_to(outfmt.outdir))

        self.remove_unknown_files(outfiles, outfmt.outdir)


def step1_exec(workdir: Path, prefix: str, infile: InputFile, outfile: Path):
    return Step1Fn.get_instance(workdir).same_as_step1_exec(prefix, infile, outfile)


class Step1Fn:
    instances = {}

    def __init__(self, workdir: Path):
        self.workdir = workdir

    @staticmethod
    def get_instance(workdir: Path):
        if workdir not in Step1Fn.instances:
            Step1Fn.instances[workdir] = Step1Fn(workdir)
        return Step1Fn.instances[workdir]

    @cache(
        backend=FileSqliteBackend.factory(filename="same_as_step1_exec.v100.sqlite"),
        cache_ser_args={
            "infile": lambda x: x.get_ident(),
        },
    )
    def same_as_step1_exec(self, prefix: str, infile: InputFile, outfile: Path):
        edges = serde.csv.deser(infile.path)
        G = nx.from_edgelist(edges[1:])
        groups = nx.connected_components(G)

        mapping = {
            f"{prefix}:{gid}": list(group) for gid, group in enumerate(groups, start=1)
        }
        serde.json.ser(mapping, outfile)
        return outfile

import logging
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import List, Literal, Type

from rich.progress import Progress, TaskID

from src.df_fetcher import PandasFetcher, PolarsFetcher
from src.df_repository import FhvTaxiRepo, GreenTaxiRepo, SQLRepo, YellowTaxiRepo, ZoneLookupRepo
from src.schemas import FhvSchema, GreenTaxiSchema, Schema, YellowTaxiSchema, ZoneLookupSchema

log = logging.getLogger("py-ingest-processor")


class Processor(metaclass=ABCMeta):
    def __init__(self, polars_ff: bool = False):
        if polars_ff:
            _fetcher = PolarsFetcher().with_schema(self.schema.polars)
        else:
            _fetcher = PandasFetcher().with_schema(self.schema.pyarrow)

        self.use_polars = polars_ff
        self.fetcher = _fetcher.with_renaming_strategy(self.renaming)

    def extract_and_load_with(
        self,
        repo: SQLRepo,
        endpoints: List[str],
        write_disposition: Literal["replace", "append"],
        tasks: List[int],
        progress,
    ):
        if not endpoints:
            return

        endpoint, *remain_endpoints = endpoints
        tid, *remain_tasks = tasks

        record = self.fetcher.fetch(endpoint)
        df_slice, *other_slices = record.slices
        completeness, total_parts = 1, len(record.slices)

        progress.update(task_id=tid, completed=0, total=total_parts)
        progress.start_task(task_id=tid)

        # This is required since, in 'append' mode, polars.df does not create
        # the table if it doesn't exist. It also guarantees idempotency
        repo.save(df_slice, write_disposition=write_disposition)
        progress.update(task_id=tid, completed=completeness, total=total_parts)

        for _ in repo.save_all(other_slices):
            completeness += 1
            progress.update(task_id=tid, completed=completeness, total=total_parts)

        self.extract_and_load_with(
            repo=repo,
            endpoints=remain_endpoints,
            write_disposition="append",
            tasks=remain_tasks,
            progress=progress,
        )

    def run(self, endpoints, db_settings, write_disposition, progress):
        repo = self.repo.with_config(*db_settings)
        tasks = self.gen_progress_tasks_for(endpoints, progress)
        self.extract_and_load_with(repo, endpoints, write_disposition, tasks, progress)

    @property
    @abstractmethod
    def schema(self) -> Schema:
        raise NotImplementedError()

    @property
    @abstractmethod
    def repo(self) -> Type[SQLRepo]:
        raise NotImplementedError()

    @property
    def renaming(self):
        return self.schema.rename_to

    @classmethod
    def gen_progress_tasks_for(cls, endpoints: List[str], progress: Progress) -> List[TaskID]:
        filenames = [Path(endpoint).stem for endpoint in endpoints]
        return [
            progress.add_task(name, start=False, total=float("inf"), completed=0)
            for name in filenames
        ]


class GreenTaxiProcessor(Processor):
    @property
    def repo(self) -> Type[GreenTaxiRepo]:
        return GreenTaxiRepo

    @property
    def schema(self) -> Schema:
        return GreenTaxiSchema()


class YellowTaxiProcessor(Processor):
    @property
    def repo(self) -> Type[YellowTaxiRepo]:
        return YellowTaxiRepo

    @property
    def schema(self) -> Schema:
        return YellowTaxiSchema()


class FhvProcessor(Processor):
    @property
    def repo(self) -> Type[FhvTaxiRepo]:
        return FhvTaxiRepo

    @property
    def schema(self) -> Schema:
        return FhvSchema()


class ZoneLookupProcessor(Processor):
    @property
    def repo(self) -> Type[ZoneLookupRepo]:
        return ZoneLookupRepo

    @property
    def schema(self) -> Schema:
        return ZoneLookupSchema()

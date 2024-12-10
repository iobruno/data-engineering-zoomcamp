from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Literal

from rich.progress import BarColumn, Progress, TaskID, TextColumn, TimeElapsedColumn

from app.df_fetcher import PandasFetcher, PolarsFetcher
from app.df_repository import SQLRepo
from app.schemas import FhvSchema, GreenTaxiSchema, Schema, YellowTaxiSchema, ZoneLookupSchema

progress = Progress(
    TextColumn("[bold blue]{task.description}"),
    BarColumn(),
    "Chunk: {task.completed}/{task.total}",
    "•",
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    TimeElapsedColumn(),
)


class Processor(metaclass=ABCMeta):
    def __init__(self, polars_ff: bool = False):
        if polars_ff:
            fetcher = PolarsFetcher().with_schema(self.schema.polars)
        else:
            fetcher = PandasFetcher().with_schema(self.schema.pyarrow)

        self.use_polars = polars_ff
        self.fetcher = fetcher.with_renaming_strategy(self.schema.rename_to)

    def extract_and_load_with(
        self,
        repo: SQLRepo,
        endpoints: list[str],
        write_disposition: Literal["replace", "append"],
        tasks: list[TaskID],
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

        self.extract_and_load_with(repo, remain_endpoints, "append", remain_tasks)

    def run(self, endpoints, repo, write_disposition):
        tasks = self.gen_progress_tasks_for(endpoints)
        self.extract_and_load_with(repo, endpoints, write_disposition, tasks)

    @property
    @abstractmethod
    def schema(self) -> Schema:
        raise NotImplementedError()

    @classmethod
    def gen_progress_tasks_for(cls, endpoints: list[str]) -> list[TaskID]:
        filenames = [Path(endpoint).stem for endpoint in endpoints]
        return [
            progress.add_task(name, start=False, total=float("inf"), completed=0)
            for name in filenames
        ]


class GreenTaxiProcessor(Processor):
    @property
    def schema(self) -> Schema:
        return GreenTaxiSchema()


class YellowTaxiProcessor(Processor):
    @property
    def schema(self) -> Schema:
        return YellowTaxiSchema()


class FhvProcessor(Processor):
    @property
    def schema(self) -> Schema:
        return FhvSchema()


class ZoneLookupProcessor(Processor):
    @property
    def schema(self) -> Schema:
        return ZoneLookupSchema()

import time
from collections import namedtuple
from typing import Union

from mmget.downloadspeedestimator import DownloadSpeedEstimator
from mmget.formatter import Formatter
from mmget.reporters.reporter import Reporter, ReporterItemState


ProgressItem = namedtuple(
    "ProgressItem",
    [
        "id",
        "title",
        "estimator",
        "state",
        "last_reported_at",
        "last_reported_progress",
    ],
)


class PrintReporter(Reporter):
    def __init__(self, elapsed_threadhold=10, completed_threadhold=10):
        self.progress_items = []
        self.elapsed_threadhold = elapsed_threadhold
        self.completed_threadhold = completed_threadhold

    def print(self, id: int, message: str):
        progress_item = self.progress_items[id]
        title = progress_item.title
        if title is None:
            print(f"{id}:{message}")
        else:
            print(f"{id}:{title}:{message}")

    def add_report_item(self):
        id = len(self.progress_items)
        progress_item = ProgressItem(
            id=id,
            title=None,
            estimator=DownloadSpeedEstimator(),
            state=ReporterItemState.Pending,
            last_reported_at=0,
            last_reported_progress=0,
        )
        self.progress_items.append(progress_item)
        return id

    def set_title(self, id: int, title: str):
        if 0 <= id < len(self.progress_items):
            self.progress_items[id] = self.progress_items[id]._replace(
                title=title
            )

    def set_state(self, id: int, state: ReporterItemState):
        if state == ReporterItemState.Pending:
            self.print(id, "Pending")
        elif state == ReporterItemState.AlreadyDownloaded:
            self.print(id, "File already existed")
        elif state == ReporterItemState.Completed:
            self.print(id, "Completed")

    def set_progress(self, id: int, bytes_received: int, total_bytes: int):
        completed = bytes_received / total_bytes * 100
        progress_item = self.progress_items[id]
        if completed > 100:
            completed = 100

        current_time = time.time()
        progress_item.estimator.add(completed)
        diff_elapsed = current_time - progress_item.last_reported_at
        diff_completed = completed - progress_item.last_reported_progress

        if (
            diff_elapsed > self.elapsed_threadhold
            or diff_completed > self.completed_threadhold
        ):
            self.progress_items[id] = self.progress_items[id]._replace(
                last_reported_at=current_time, last_reported_progress=completed
            )
            received_unit = Formatter.format_bytes(bytes_received)
            total_unit = Formatter.format_bytes(total_bytes)

            text = f"{received_unit} of {total_unit} ({completed:05.1f}%)"

            if completed < 100:
                eta = progress_item.estimator.get_formatted_eta()
                if eta:
                    text += f" - {eta} remaining"

            self.print(
                id,
                text,
            )

    def ask_options(self, id: int, message: str, options):
        list = ",".join(options)
        self.print(id, f"{message}: {list}")

    def start(self):
        pass

    def stop(self):
        pass

    def set_error(self, id: int, error: Union[str, Exception]):
        if isinstance(error, ValueError):
            self.print(id, "Output Path Conflict")
        elif isinstance(error, FileExistsError):
            self.print(id, "File already exists")
        else:
            self.print(id, f"Error - {error}")

    def show_message(self, id: int, message: str):
        if 0 <= id < len(self.progress_items):
            self.print(id, message)

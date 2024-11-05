import asyncio
import os
from mmget.outputpathvalidator import OutputPathValidator
from mmget.reporters.reporterfactory import ReporterFactory
from mmget.tasks.taskfactory import TaskFactory
from mmget.reporters.threadsafereporter import ThreadSafeProgressReporter
from mmget.threadpool import ThreadPool


class Downloader:
    def __init__(
        self,
        hf_token=None,
        civitai_token=None,
        max_workers=5,
        reporter=None,
        dest=None,
        dest_type=None,
    ):
        self.reporter = reporter
        self.thread_safe_reporter = ThreadSafeProgressReporter(
            self.reporter, asyncio.get_event_loop()
        )
        self.tasks = []
        self.hf_token = (
            hf_token if hf_token is not None else os.getenv("MMGET_HF_TOKEN")
        )
        self.civitai_token = (
            civitai_token
            if civitai_token is not None
            else os.getenv("MMGET_CIVITAI_TOKEN")
        )
        self.dest = dest if dest is not None else os.getenv("MMGET_DEST_PATH")
        self.dest_type = (
            dest_type if dest_type is not None else os.getenv("MMGET_DEST_TYPE")
        )
        self._futures = None
        ThreadPool.get_instance().set_max_workers(max_workers)

    def dl(self, url: str, dest=None, dest_type=None, version=None):
        id = len(self.tasks)
        dest = dest if dest is not None else self.dest
        dest_type = dest_type if dest_type is not None else self.dest_type
        output_path = OutputPathValidator(dest, dest_type=dest_type)
        task = TaskFactory.create(
            id,
            url,
            reporter=self.thread_safe_reporter,
            output_path=output_path,
            hf_token=self.hf_token,
            civitai_token=self.civitai_token,
            version=version,
        )
        self.tasks.append(task)
        return self

    def create_tasks(self):
        if self._futures is not None:
            raise RuntimeError(
                "mmget.create_tasks() has already been called - cannot call it multiple times"  # noqa
            )
        self._futures = [task.run() for task in self.tasks]
        return asyncio.gather(*self._futures)

    def run(self):
        if self._futures is not None:
            raise RuntimeError(
                "mmget.run() has already been called - cannot call it multiple times"
            )
        if self.reporter is None:
            self.reporter = ReporterFactory.create()
        for _ in range(len(self.tasks)):
            self.reporter.add_report_item()
        self.thread_safe_reporter.set_reporter(self.reporter)
        self.reporter.start()
        loop = asyncio.get_event_loop()

        async def run_and_stop():
            await self.create_tasks()
            self.reporter.stop()

        if loop.is_running():
            loop.create_task(run_and_stop())
        else:
            loop.run_until_complete(run_and_stop())


def mmget(*args, **kwargs):
    """
    Download file from various sources including regular URLs, Hugging Face, and Civitai.

    Args:
        url (str): The URL of the file to download.
        *paths (str): The local path(s) where the file should be saved.
    """  # noqa
    return Downloader(*args, **kwargs)

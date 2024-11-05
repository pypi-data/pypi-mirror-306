from mmget.tasks.task import Task
import asyncio


class InvalidTask(Task):
    def __init__(self, id, url, reporter, output_path, error_message=None):
        self.error_message = (
            "Invalid URL" if error_message is None else error_message
        )
        super().__init__(id, url, reporter, output_path)

    def run(self, options=None) -> "asyncio.Future":
        self.reporter.set_title(self.id, self.url)
        self.reporter.set_error(self.id, self.error_message)
        self.future.set_result(None)
        return self.future

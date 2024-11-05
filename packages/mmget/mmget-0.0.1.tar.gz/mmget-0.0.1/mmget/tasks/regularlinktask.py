import os
import requests
from mmget.tasks.task import Task
from mmget.partedfilewriter import PartedFileWriter
from mmget.url import HeaderReader
import asyncio


class RegularLinkTask(Task):
    def worker(self):
        try:
            response = requests.get(self.url, stream=True)
            response.raise_for_status()
            output = self.output_path.absolute_path

            if self.output_path.is_directory:
                header_reader = HeaderReader(response.headers, self.url)
                filename = header_reader.get_filename()
                output = os.path.join(output, filename)

            file_manager = PartedFileWriter.get_instance()

            with file_manager.open(output) as file:
                file_manager.transfer_response_to_file(
                    response,
                    file,
                    self.id,
                    self.reporter,
                )
            self.future.set_result(None)

        except Exception as e:
            self.reporter.set_error(self.id, e)
            self.future.set_result(e)

    def run(self, options=None) -> "asyncio.Future":
        self.reporter.set_title(self.id, self.url)

        self.submit_worker(self.worker)

        return self.future

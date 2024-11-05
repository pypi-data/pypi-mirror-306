import asyncio
import os

from mmget.reporters.reporter import ReporterItemState
from mmget.tasks.task import Task
from mmget.partedfilewriter import PartedFileWriter
from mmget.url import HeaderReader, URLReader
import requests


class HuggingFaceTask(Task):
    def __init__(self, id, url, reporter, output_path, hf_token=None):
        # Parse the URL to extract repo_id and filename
        parsed_url = URLReader(url)
        self.hf_token = hf_token

        if not parsed_url.is_hf:
            raise ValueError("Invalid Hugging Face dataset URL")

        repo_id = parsed_url.hf_repo_id
        filename = parsed_url.hf_filename
        revision = parsed_url.hf_revision

        super().__init__(
            id, f"https://huggingface.co/{repo_id}", reporter, output_path
        )
        self.repo_id = repo_id
        self.filename = filename
        self.revision = revision

    def worker(self):
        try:
            self.reporter.set_title(self.id, f"{self.repo_id}/{self.filename}")
            self.reporter.set_state(self.id, ReporterItemState.Downloading)
            url = f"https://huggingface.co/{self.repo_id}/resolve/{self.revision}/{self.filename}"  # noqa

            headers = {}
            if self.hf_token is not None:
                headers = {"Authorization": f"Bearer {self.hf_token}"}

            file_manager = PartedFileWriter.get_instance()

            response = requests.get(url, stream=True, headers=headers)
            response.raise_for_status()
            output = self.output_path.absolute_path

            if self.output_path.is_directory:
                header_reader = HeaderReader(response.headers, self.url)
                filename = header_reader.get_filename()
                output = os.path.join(output, filename)

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
        self.submit_worker(self.worker)
        return self.future

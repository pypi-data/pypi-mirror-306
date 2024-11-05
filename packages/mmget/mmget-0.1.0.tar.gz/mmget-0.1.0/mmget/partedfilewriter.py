import os
import threading
import re
from mmget.reporters.reporter import ReporterItemState
from mmget.errors import ConflictOutputError

instance = None
parted_suffix = ".part"


class PartedFileWriter:
    """
    Manage file to be saved
    """

    def __init__(self):
        self.writing_files = {}
        self.lock = threading.Lock()

    @staticmethod
    def get_instance():
        global instance
        if instance is None:
            instance = PartedFileWriter()
        return instance

    from contextlib import contextmanager

    @contextmanager
    def open(self, absolute_path: str):
        with self.lock:
            if absolute_path in self.writing_files:
                raise ConflictOutputError()

            if os.path.exists(absolute_path):
                raise FileExistsError(f"File '{absolute_path}' already exists.")

            parted_path = absolute_path + parted_suffix

            try:
                file = open(parted_path, "wb")
                self.writing_files[absolute_path] = file
                yield file
            except FileNotFoundError:
                raise Exception(f"Unable to write the file: {parted_path}")

            file.close()
            if absolute_path in self.writing_files:
                del self.writing_files[absolute_path]
            if os.path.exists(parted_path):
                os.rename(parted_path, absolute_path)

    def transfer_response_to_file(
        self, response, file, id: int, reporter, block_size=131072
    ):
        total_size = int(response.headers.get("content-length", 0))
        bytes_received = 0

        for data in response.iter_content(block_size):
            size = file.write(data)
            bytes_received += size
            reporter.set_progress(id, bytes_received, total_size)

        reporter.set_state(id, ReporterItemState.Completed)
        reporter.show_message(
            id, f"Saved at {re.sub(parted_suffix + '$', '', file.name)}"
        )

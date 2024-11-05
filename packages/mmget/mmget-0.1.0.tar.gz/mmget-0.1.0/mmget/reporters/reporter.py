from abc import ABC, abstractmethod
from enum import Enum
from typing import Union


class ReporterItemState(str, Enum):
    Pending = "Pending"
    Completed = "Completed"
    Downloading = "Downloading"
    AlreadyDownloaded = "AlreadyDownloaded"
    Error = "Error"


class Reporter(ABC):
    @abstractmethod
    def add_report_item(self) -> int:
        pass

    @abstractmethod
    def set_title(self, id: int, title: str):
        pass

    @abstractmethod
    def set_state(self, id: int, state: ReporterItemState):
        pass

    @abstractmethod
    def set_progress(self, id: int, bytes_received: int, total_bytes: int):
        pass

    @abstractmethod
    def show_message(self, id: int, message: str):
        """
        Show a message for a specific report item
        """
        pass

    def ask_options(self, id: int, message: str, options, callback):
        pass

    def can_ask_options(self) -> bool:
        """
        This function should be threadsafe
        """
        return False

    @abstractmethod
    def start(self):
        """
        Start the reporter
        """
        pass

    @abstractmethod
    def stop(self, message: str = None):
        """
        Stop the reporter
        """
        pass

    @abstractmethod
    def set_error(self, id: int, error: Union[str, Exception]):
        """
        Set an error message for a specific report item
        """
        pass

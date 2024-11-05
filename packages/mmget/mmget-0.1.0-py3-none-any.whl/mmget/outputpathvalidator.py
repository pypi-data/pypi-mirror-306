import os
from mmget.types import DistType


class OutputPathValidator:
    def __init__(self, dest, dest_type=None):
        if dest is None:
            dest = os.getcwd()
        self.absolute_path = os.path.abspath(dest)
        self.dest_type = dest_type
        self.error_message = None
        self.is_directory = os.path.isdir(self.absolute_path)
        self.is_exists = os.path.exists(self.absolute_path)
        self._validate()

    def _validate(self):
        self.is_valid = False
        is_dist_type_valid = self.dest_type is None or self.dest_type in [
            item.value for item in DistType
        ]
        if not is_dist_type_valid:
            self.error_message = f"Invalid dest_type argument: {self.dest_type}"
            return

        if not (
            (self.is_directory and self.is_exists)
            if is_dist_type_valid and self.dest_type is not None
            else True
        ):
            self.error_message = (
                f"The output path is not a valid {self.dest_type} folder"
            )
            return

        self.is_valid = True

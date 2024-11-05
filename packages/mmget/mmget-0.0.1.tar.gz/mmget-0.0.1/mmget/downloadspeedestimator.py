from collections import namedtuple
import time

Record = namedtuple("Record", ["time", "progress"])


class DownloadSpeedEstimator:
    def __init__(self):
        self.start_time = None
        self.records = []
        self.eta = None
        self.completed_time = None
        self.add_record_threshold = 1
        self.record_limit = 60
        self.eta_threshold = 60

    def get_last_record(self):
        return self.records[-1]

    def add(self, progress):
        if self.completed_time is not None:
            # Estimation completed
            return
        current_time = time.time()
        if self.start_time is None:
            self.start_time = current_time

        new_record = Record(time=current_time, progress=progress)
        if len(self.records) < 2:
            # Keep the first 2 records
            self.records.append(new_record)
        else:
            # Compare the last 2 records instead of the last one
            reference_record = self.records[-2]
            if current_time - reference_record.time > self.add_record_threshold:
                self.records.append(new_record)
            else:
                self.records[-1] = new_record

        self.records = self.records[-self.record_limit :]
        if progress >= 100:
            self.eta = 0
            self.completed_time = current_time
        else:
            self.eta = self.calculate_eta(progress, current_time)

    def calculate_eta(self, progress, current_time):
        positive_records = [
            r
            for r in self.records
            if (current_time - self.eta_threshold - r.time) > 0
        ]
        if positive_records:
            record = positive_records[-1]
        else:
            record = self.records[0]

        elapsed_time = current_time - record.time
        progress_diff = progress - record.progress

        if progress_diff > 0:
            time_per_percent = elapsed_time / progress_diff
            remaining_percentage = 100 - progress
            return time_per_percent * remaining_percentage
        return None

    def get_formatted_eta(self):
        if self.eta is None:
            return ""

        eta_seconds = int(self.eta)
        minutes, seconds = divmod(eta_seconds, 60)
        hours, minutes = divmod(minutes, 60)

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

import os
import time
from urllib.parse import urlparse, parse_qsl
from mmget.tasks.task import Task
import asyncio


class DummyTask(Task):
    def worker(self, options):
        parsed_url = urlparse(self.url)
        query_params = dict(parse_qsl(parsed_url.query))
        sleep_time = int(query_params.get("s", 10))
        ask_options = bool(
            query_params.get("ask_options", "").lower() == "true"
        )

        stop = query_params.get("stop", None)
        if stop is not None:
            stop = int(stop)

        selected_option = options.get("selected_option", None)
        title = options.get("title", "")

        try:
            if ask_options and selected_option is None:
                if self.reporter.can_ask_options():

                    def on_option_selected(_value):
                        new_options = {
                            **options,
                            "selected_option": _value,
                        }
                        self.run(new_options)

                    self.reporter.ask_options(
                        self.id, "Ask", ["a", "b", "c"], on_option_selected
                    )
                else:
                    self.reporter.show_message(
                        self.id, "Available opions: a, b, c"
                    )
                    self.future.set_result(None)
                return

            if selected_option is not None:
                title = title + ":" + selected_option
                self.reporter.set_title(self.id, title)

            elapsed = 0
            bytes_recevied = 0
            total_bytes = 1024 * 1024
            step = int(total_bytes / sleep_time)
            while bytes_recevied < total_bytes:
                time.sleep(1)
                elapsed = elapsed + 1
                bytes_recevied = bytes_recevied + step
                bytes_recevied = min(total_bytes, bytes_recevied)
                self.reporter.set_progress(self.id, bytes_recevied, total_bytes)

                if stop and bytes_recevied >= total_bytes:
                    while True:
                        time.sleep(1000000)

            self.future.set_result(None)

        except Exception as e:
            self.reporter.set_error(self.id, e)
            self.future.set_result(e)

    def run(self, options=None) -> "asyncio.Future":
        options = options or {}
        parsed_url = urlparse(self.url)
        path = parsed_url.path
        domain = parsed_url.netloc
        if path:
            title = os.path.basename(path)
        elif domain:
            title = domain
        else:
            title = self.url
        self.reporter.set_title(self.id, title)

        options["title"] = title
        self.submit_worker(self.worker, options)

        return self.future

import asyncio

from mmget.threadpool import ThreadPool


class Task:
    def __init__(self, id, url, reporter, output_path):
        self.id = id
        self.url = url
        self.reporter = reporter
        self.output_path = output_path
        self.future = asyncio.Future()

    def get_event_loop(self):
        try:
            thread_loop = asyncio.get_event_loop()
        except RuntimeError:
            thread_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(thread_loop)
        return thread_loop

    def run(self, options=None) -> "asyncio.Future":
        """Run the task and return a future

        Args:
            options: Optional dictionary containing task options
        """
        raise NotImplementedError("Task.run() is not implemented")

    def submit_worker(self, worker, *args):
        """Submit a worker function to be run in a thread pool

        Args:
            worker: The worker function to run
        """
        ThreadPool.get_instance().get_thread_pool().submit(worker, *args)

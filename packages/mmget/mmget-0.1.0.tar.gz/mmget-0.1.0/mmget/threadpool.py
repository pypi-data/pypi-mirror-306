from concurrent.futures import ThreadPoolExecutor


thread_pool = None
instance = None


class ThreadPool:
    def __init__(self, max_workers=5):
        self.max_workers = max_workers
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)

    def set_max_workers(self, max_workers):
        if self.max_workers != max_workers:
            self.thread_pool.shutdown(wait=True)
            self.max_workers = max_workers
            self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)

    @staticmethod
    def get_instance():
        global instance
        if instance is None:
            instance = ThreadPool()
        return instance

    def get_thread_pool(self):
        return self.thread_pool

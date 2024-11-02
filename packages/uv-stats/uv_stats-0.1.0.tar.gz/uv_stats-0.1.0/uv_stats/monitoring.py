import time
from contextlib import contextmanager


class MonitoringStorage(object):
    def __init__(self) -> None:
        pass

    @contextmanager
    def run_context_manager(self):
        stated_at = time.time()
        yield
        time.time() - stated_at

    @contextmanager
    def query_context_manager(self):
        stated_at = time.time()
        yield
        time.time() - stated_at

    @contextmanager
    def print_context_manager(self):
        stated_at = time.time()
        yield
        time.time() - stated_at

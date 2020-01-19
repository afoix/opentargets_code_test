from multiprocessing import Process, Value
import ctypes

def run_work_method(self):
    self.work()

class BaseStep:
    def __init__(self):
        self._process = Process(target=run_work_method, args=(self,))
        self._progress = Value(ctypes.c_uint64, lock=False)

    def start(self):
        self._process.start()

    @property
    def progress(self):
        return self._progress.value

    def wait_for_exit(self, poll_interval = 1, progress_action = None):
        while self._process.is_alive():
            self._process.join(timeout=poll_interval)
            if progress_action is not None:
                progress_action()
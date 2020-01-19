from sys import stderr
from time import time

class ProgressReporter:

    def __init__(self):
        self.start_time = time()
        stderr.write('\n')

    def next_step(self):
        stderr.write('\n')
        stderr.flush()

    def display(self, info):
        stderr.write('\r                                                                                                           ')
        stderr.write(f'\r  [{self.elapsed_seconds}s] {info}')        
        stderr.flush()

    @property
    def elapsed_seconds(self):
        return int(time() - self.start_time)
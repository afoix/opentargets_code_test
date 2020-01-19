from base import BaseStep
from multiprocessing import Queue
import gzip

class DecompressorStep(BaseStep):
    '''The Decompressor decompresses a gzipped text file and pushes each line of text onto a queue.'''

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.output = Queue()
        self.limit = None # This is useful for testing
        self.start()

    def work(self):
        file = gzip.open(self.filename)

        while True:
            line = file.readline()

            if line == b'' or (self.limit != None and self._progress.value >= self.limit):
                break            

            self.output.put(line)
            self._progress.value += 1
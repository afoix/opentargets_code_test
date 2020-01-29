from base import BaseStep
import json

class ParserAndRouterStep(BaseStep):
    '''A ParserAndRouter takes a line of JSON text from a shared queue, parses it, and extracts the specific values
    we are interested in. It then 'buckets' the data into one of a number of output queues, to balance the load.'''

    def __init__(self, input, outputs, extract_data, get_bucket_index):
        super().__init__()
        self.input = input
        self.outputs = outputs
        self.extract_data = extract_data
        self.get_bucket_index = get_bucket_index
        self.start()

    def work(self):

        while True:

            line = self.input.get()            
            if line == None:
                break            

            j = json.loads(line)
            
            data = self.extract_data(j)
            bucket = self.get_bucket_index(data) % len(self.outputs)

            self.outputs[bucket].put(data)
            self._progress.value += 1
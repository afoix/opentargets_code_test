from base import BaseStep
from multiprocessing import Queue
from math import floor

class TargetDiseaseScoreCollectorStep(BaseStep):
    '''A TargetDiseaseScoreCollector recives tuples of target/disease/score in an input queue, and once the queue is empty, 
    calculates the median and top3 scores for each target/disease combination, sorts them by median score in ascending order, 
    and writes them to an output queue.'''

    def __init__(self):
        super().__init__()
        self.input = Queue()
        self.output = Queue()
        self.start()

    def work(self):

        results = {}

        # read and store all the data
        while True:
            read = self.input.get()
            if read == None:
                break

            (target_id, disease_id, association_score) = read

            diseases = results.setdefault(target_id, {})
            samples = diseases.setdefault(disease_id, [])
            samples.append(association_score)

            self._progress.value += 1

        # the data finished, so now make the results
        result_tuples = []

        for (target_id, diseases) in results.items():
            for (disease_id, samples) in diseases.items():

                samples.sort()

                median = samples[floor((len(samples) + 1) / 2) - 1]
                top3 = ','.join([str(s) for s in samples[-3:]])

                result_tuples.append((target_id, disease_id, median, top3))

        result_tuples.sort(key=(lambda t: t[2]))

        for t in result_tuples:
            self.output.put(t)

        self.output.put(None)
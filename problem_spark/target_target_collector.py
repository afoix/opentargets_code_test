from base import BaseStep
from multiprocessing import Queue, Value, Pool, RawArray, cpu_count
from math import ceil
import ctypes

# multiprocessing requires that these are global
target_diseases = None
target_matcher_progress = None

def initState(arr, progress):
    global target_diseases, target_matcher_progress
    target_diseases = arr
    target_matcher_progress = progress

def get_diseases_for_target(target_index, max_diseases_per_target):
    global target_diseases
    result = set()
    for i in range(max_diseases_per_target):
        disease_index = target_diseases[target_index * max_diseases_per_target + i]
        if disease_index == 0:
            break
        result.add(disease_index)
    return result

def count_paired_targets(num_targets, max_diseases_per_target, from_index, to_index):
    global target_matcher_progress
    total_matches = 0
    for target_index in range(from_index, to_index):
        target_diseases = get_diseases_for_target(target_index, max_diseases_per_target)

        for other_target_index in range(num_targets):
            other_target_diseases = get_diseases_for_target(other_target_index, max_diseases_per_target)

            if len(target_diseases & other_target_diseases) > 1:
                total_matches += 1    

        with target_matcher_progress.get_lock():
            target_matcher_progress.value += 1
            
    return total_matches

class TargetTargetCollector(BaseStep):
    '''The TargetTargetCollector takes a stream of (target_id, disease_id) tuples identifies
    which target_ids share at least two disease_ids.'''

    def __init__(self):
        super().__init__()
        self.input = Queue()
        self.output = Value(ctypes.c_uint64, lock=True)
        self.total_targets = Value(ctypes.c_uint64, lock=False)
        self.scan_progress = Value(ctypes.c_uint64, lock=True)
        self.start()

    def work(self):

        target_indices = {}
        disease_indices = {}

        seen = []
        max_diseases_per_target = 0

        while True:
            read = self.input.get()
            if read == None:
                break

            (target_id, disease_id) = read

            target_index = target_indices.setdefault(target_id, len(target_indices))
            disease_index = disease_indices.setdefault(disease_id, len(disease_indices) + 1)

            if target_index == len(seen):
                seen.append(set())
            seen[target_index].add(disease_index)
            max_diseases_per_target = max(max_diseases_per_target, len(seen[target_index]))

            self._progress.value += 1

        shared_array = RawArray(ctypes.c_uint32, len(target_indices) * max_diseases_per_target)

        next_free_target = 0
        for target_index in range(len(target_indices)):
            diseases = seen[target_index]

            # If this target has fewer than 2 diseases, it cannot possibly have 2+ matches
            if len(diseases) < 2:
                continue

            idx = 0
            for disease_index in diseases:
                shared_array[next_free_target * max_diseases_per_target + idx] = disease_index
                idx += 1
            next_free_target += 1

        num_targets = next_free_target
        self.total_targets.value = num_targets

        processcount = cpu_count()
        chunk_size = ceil(num_targets / processcount)
        with Pool(initializer=initState, initargs=(shared_array, self.scan_progress), processes = processcount) as pool:
    
            results = []
            for i in range(processcount):

                from_index = i * chunk_size
                to_index = min((i+1) * chunk_size, num_targets)

                results.append(pool.apply_async(count_paired_targets, [num_targets, max_diseases_per_target, from_index, to_index]))
    
            for result in results:
                self.output.value += result.get()
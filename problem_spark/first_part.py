from decompressor import DecompressorStep
from parser_and_router import ParserAndRouterStep
from score_collector import TargetDiseaseScoreCollectorStep
from progress_reporter import ProgressReporter

def merge_sorted_queues(queues):
    nexts = {}
    for q in queues:
        n = q.get()
        if n != None:
            nexts[q] = n

    while True:
        if len(nexts) == 0:
            break
        (k, v) = min(nexts.items(), key=(lambda v: v[1][2]))
        yield v
        nexts[k] = k.get()
        if nexts[k] == None:
            del nexts[k]          

def get_data_from_json(json):
    target_id = json["target"]["id"]
    disease_id = json["disease"]["id"]
    association_score = json["scores"]["association_score"]
    return (target_id, disease_id, association_score)

def get_tuple_bucket_key(t):
    return hash(t[0])

if __name__ == '__main__':

    progress = ProgressReporter()

    decompressor = DecompressorStep('17.12_17.12_evidence_data.json.gz')
    collectors = [TargetDiseaseScoreCollectorStep() for _ in range(8)]
    routers = [ParserAndRouterStep(decompressor.output, [c.input for c in collectors], get_data_from_json, get_tuple_bucket_key) for _ in range(4)]

    # Wait for the decompressor to finish
    decompressor.wait_for_exit(progress_action=lambda: progress.display(f'Decompressed: {decompressor.progress} records'))
    progress.next_step()

    # Send stop signal for each router
    for router in routers:
        router.input.put(None)

    # Wait for them to stop
    for router in routers:
        router.wait_for_exit(progress_action=lambda: progress.display(f'Parsed: {sum([r.progress for r in routers])} Collected: {sum([c.progress for c in collectors])}'))
    progress.next_step()

    # Send stop signal to each collector
    for collector in collectors:
        collector.input.put(None)

    for (targetId, diseaseId, median, top3) in merge_sorted_queues([c.output for c in collectors]):
        print(f'{targetId},{diseaseId},{median},{top3}')

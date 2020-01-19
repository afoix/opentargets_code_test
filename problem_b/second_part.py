from decompressor import DecompressorStep
from parser_and_router import ParserAndRouterStep
from progress_reporter import ProgressReporter
from target_target_collector import TargetTargetCollector

def get_data_from_json(json):
    targetID = json["target"]["id"]
    diseaseID = json["disease"]["id"]
    return (targetID, diseaseID)

def get_tuple_bucket_key(t):
    return hash(t[0])

if __name__ == '__main__':

    progress = ProgressReporter()

    decompressor = DecompressorStep('17.12_17.12_evidence_data.json.gz')
    collector = TargetTargetCollector()
    routers = [ParserAndRouterStep(decompressor.output, [collector.input], get_data_from_json, get_tuple_bucket_key) for _ in range(4)]

    # Wait for the decompressor to complete
    decompressor.wait_for_exit(progress_action=lambda: progress.display(f'{decompressor.progress} records decompressed'))

    total_records = decompressor.progress
    progress.next_step()

    # Send stop signal for each router
    for router in routers:
        router.input.put(None)

    # Wait for them to stop
    for router in routers:
        router.wait_for_exit(progress_action=lambda: progress.display(f'{sum([r.progress for r in routers])}/{total_records} records parsed'))

    progress.next_step()

    # Send stop signal to collector
    collector.input.put(None)
    collector.wait_for_exit(progress_action=lambda: progress.display(f'Scanned {collector.scanProgress.value}/{collector.total_targets.value} targets for matches'))

    progress.next_step()

    print (f'\n\nFound {collector.output.value} total target-target pairs with at least 2 diseases in common in {progress.elapsed_seconds} seconds.\n\n')


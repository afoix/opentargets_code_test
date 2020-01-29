# Problem B - parse a JSON dump

This is a Python tool to parse an OpenTargets JSON dump in gzip format.

The tool requires Python 3.8.

The tool expects a gzipped data file named '17.12_17.12_evidence_data.json.gz' to be present in the current directory.

## Part 1 - Compute association scores

The first part of the tool computes the median and top 3 association score values for each target/disease pair. The results are written to standard output in CSV format.

Run it like this:

> `python first_part.py > results.csv`

Progress information is displayed on stderr, while the end results will be written to the CSV file. The CSV output for the test data provided is [available here](https://drive.google.com/file/d/1U9D3vDoLYzXNpUzJbeu2C18cCX4qgWI6/view?usp=sharing).

The tool uses Python `multiprocessing` and spawns multiple child processes to do work in parallel:

* One `Decompressor` process decompresses the input file and feeds each line of the input onto a queue.
* Four `ParserAndRouter` processes read lines from the queue, parse the JSON data, and extract the target ID, disease ID, and association score. This data is then 'bucketed' into one of a number of queues, to balance the load.
* Eight `TargetDiseaseScoreCollector` processes, one for each of the load balanced queues, receieve the target ID / disease ID / score tuples, and group them by target/disease.

After all the data is processed, each collector calculates the median score and top 3 scores for each target/disease pair, and pushes its results into an output queue, sorted in ascending order of median score. The main process then reads from all these output queues and merges the results to produce the final output.

## Part 2 - compute target-target pairs

The second part of the tool computes the number of target-target pairs in the input data which have two or more diseases in common. The final count is written to standard output.

Run it like this:

> `python second_part.py`

The output for the provided test data looks like this:

```
> python second_part.py

  [531s] 5784597 records decompressed
  [531s] 5784597/5784597 records parsed
  [1963s] Scanned 33109/33109 targets for matches

Found 242253818 total target-target pairs with at least 2 diseases in common in 1963 seconds.
```

The tool reuses the `Decompressor` and `ParserAndRouter` components from Part 1, though this time it only extracts the target ID and disease ID, and the load balancing is not used. The (target ID, disease ID) tuples are fed to a single `TargetTargetCollector`, which maps the target ID and disease ID to numeric indices, and groups the values by target ID.

When all the data is processed, the `TargetTargetCollector` creates a shared memory array and populates it with the disease indices for each target. Then it spawns a pool of child processes which each take a section of the array, and check the targets in that section against all other targets to find ones that share 2 or more diseases. The result for each section is returned to the `TargetTargetCollector`, which adds them and returns them to the main program.
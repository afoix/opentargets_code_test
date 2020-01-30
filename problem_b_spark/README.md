# Problem B - parse a JSON dump (Apache Spark version)

This is a Python tool to parse an OpenTargets JSON dump in gzip format.

The tool requires Apache Spark, Python 3.8, and the pyspark module (install with `pip install pyspark`).

## Part 1 - Compute association scores

The first part of the tool computes the median and top 3 association score values for each target/disease pair.

Run it like this:

> `spark-submit part1.py --input path/to/input.json.gz --output path/to/output`

The tool will read all the JSON records from the input file, and write the final CSV data to the given output directory.

It uses a Spark pipeline which:
* Reads lines from the input file
* Parses the JSON and extracts the target ID, disease ID, and association score
* Groups all the results by (target ID, disease ID) to collect all the samples for that pair
* Calculates the median and top 3 samples for each pair
* Sorts by median in ascending order
* Creates a CSV line
* Writes the CSV line to the result

Progress information is displayed on stderr, while the end results will be written to the CSV file. The CSV output for the test data provided is [available here](https://drive.google.com/file/d/1U9D3vDoLYzXNpUzJbeu2C18cCX4qgWI6/view?usp=sharing).

## Part 2 - compute target-target pairs

The second part of the tool computes the number of target-target pairs in the input data which have two or more diseases in common. The final count is written to standard output.

Run it like this:

> `spark-submit part1.py --input path/to/input.json.gz`

The tool uses a Spark pipeline which:

* Reads lines from the input file
* Parses the JSON and extracts the target ID and disease ID
* Groups results by disease ID
* Discards diseases which only have one target, because that means the disease cannot be in common
* For each disease, generates a (target, target) pair for all targets associated with that disease
* Counts how many times every (target, target) pair is seen
* Discards pairs which were only seen once
* Counts the remaining pairs and displays the result

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

## Part 2 - compute target-target pairs

The second part of the tool computes the number of target-target pairs in the input data which have two or more diseases in common. The final count is written to standard output.

Run it like this:

> `spark-submit --driver-memory 16g --conf spark.driver.maxResultSize=2g part2.py --input path/to/input.json.gz`

The tool uses Spark DataFrames to compute the result. It will run on your local machine and use all available cores.

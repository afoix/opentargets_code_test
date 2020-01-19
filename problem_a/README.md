# Problem A - query a REST API

This is a Python tool to query the OpenTargets API and calculate some statistics for a given target or disease.

The tool requires Python 3.8. It also requires the `requests` module, which can be installed through `pip`.

## Usage

There are three usage modes:

* `python my_coding_test.py -t <target_id>` will show statistics for the given target.
* `python my_coding_test.py -d <disease_id>` will show statistics for the given disease.
* `python my_coding_test.py --test` will run integration tests.

The statistics displayed are the minimum, maximum, average, and standard deviation of the association scores for the given target or disease.

## Structure

The program has two main classes:

* `ProgramSettings` contains the settings for one run of the program, and is created from the command line arguments.
* `OverallAssociationScoreQuery` queries the REST API, collects the association scores, and calculates the statistics.


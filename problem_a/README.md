# Problem A - query a REST API

This is a Python tool to query the OpenTargets API and calculate some statistics for a given target or disease.

The tool requires Python 3.8. It also requires the `requests` module, which can be installed through `pip`.

## Usage

There are three usage modes:

* `python my_code_test.py -t <target_id>` will show statistics for the given target.
* `python my_code_test.py -d <disease_id>` will show statistics for the given disease.
* `python my_code_test.py --test` will run integration tests.

The statistics displayed are the minimum, maximum, average, and standard deviation of the association scores for the given target or disease.

## Example usage

```
> python my_code_test.py -t ENSG00000157764
samples: 2488; min: 0.004; max: 1.0; average: 0.34045252880249316; stddev: 0.33960804100533276

> python my_code_test.py -d EFO_0002422
samples: 5290; min: 2.0284133805165937e-06; max: 1.0; average: 0.12537729136042894; stddev: 0.19757689578541335

> python my_code_test.py -d EFO_0000616 
samples: 16236; min: 8.090567619191111e-06; max: 1.0; average: 0.4099037689025387; stddev: 0.3367559859013396

> python my_code_test.py --test        
...
----------------------------------------------------------------------
Ran 3 tests in 6.194s

OK
```

## Structure

The program has two main classes:

* `ProgramSettings` contains the settings for one run of the program, and is created from the command line arguments.
* `OverallAssociationScoreQuery` queries the REST API, collects the association scores, and calculates the statistics.


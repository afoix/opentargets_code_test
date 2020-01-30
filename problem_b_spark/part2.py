from pyspark import SparkContext
from operator import add
import json, math, argparse, pathlib, itertools
sc = SparkContext("local", "part two")

parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='input', required=True)
args = parser.parse_args()

inputUri = pathlib.Path(args.input).resolve().as_uri()

def getTuple(s):
    '''Take a line of JSON, parse it, and extract the values we are interested in'''
    j = json.loads(s)
    return (j["disease"]["id"], j["target"]["id"])

# Load and parse the data and build (disease, [target, target, target...]) groups
# Keep only diseases that have more than one target
diseaseTargetAssociations = sc.textFile(inputUri) \
  .map(getTuple) \
  .groupByKey() \
  .filter(lambda t: len(t[1]) > 1)

def generateTargetTargetPairs(tuple):
    targets = list(tuple[1])
    targets.sort()
    for i, targetA in enumerate(targets):
        for targetB in targets[i:]:
            yield f'{targetA} {targetB}'

# For each disease, generate (targetA, targetB) tuples for all targets associated with that disease
targetTargetAssociations = diseaseTargetAssociations \
  .flatMap(generateTargetTargetPairs)

# Count how many times we have seen each (targetA, targetB) tuple  
targetAssociationCounts = targetTargetAssociations.countByValue()

# Count how many we see more than 1 time
result = list(filter(lambda t: t[1] > 1, targetAssociationCounts.items()))

print(len(result))
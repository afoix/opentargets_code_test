from pyspark import SparkContext
import json, math, argparse, pathlib
sc = SparkContext("local", "part one")

parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='input', required=True)
parser.add_argument('--output', dest='output', required=True)
args = parser.parse_args()

inputUri = pathlib.Path(args.input).resolve().as_uri()
outputUri = pathlib.Path(args.output).resolve().as_uri()

def getTuple(s):
    '''Take a line of JSON, parse it, and extract the values we are interested in'''
    j = json.loads(s)
    return ((j["target"]["id"], j["disease"]["id"]), j["scores"]["association_score"])

def getMedianAndTop3(kvp):
    '''Take the samples for a target/disease pair, and calculate the median and top 3'''
    ((targetID, diseaseID), valuesIterable) = kvp
    values = list(valuesIterable)
    values.sort()
    median = values[math.floor((len(values) + 1) / 2) - 1]
    return (median, (targetID, diseaseID, values[-3:]))

def makeCsvLine(kvp):
    '''Turn the data into a line of the CSV file'''
    (median, (targetID, diseaseID, top3)) = kvp
    top3Csv = ', '.join([str(s) for s in top3])
    return f'{targetID}, {diseaseID}, {median}, {top3Csv}'

sc.textFile(inputUri) \
  .map(getTuple) \
  .groupByKey() \
  .map(getMedianAndTop3) \
  .sortByKey(ascending=True) \
  .map(makeCsvLine) \
  .saveAsTextFile(outputUri)
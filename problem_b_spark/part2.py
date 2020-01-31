from pyspark import SparkContext
from pyspark.sql import SparkSession, Row
from pyspark.sql import functions as F
import argparse, pathlib
sc = SparkContext("local[*]", "part two")
spark = SparkSession(sc)

parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='input', required=True)
args = parser.parse_args()

inputUri = pathlib.Path(args.input).resolve().as_uri()

df = spark.read.json(inputUri)
df = df.select(df.disease.id.alias('disease'), df.target.id.alias('target'))
df = df.repartition('disease')

targetPairs = df.alias("a").join(df.alias("b"), F.col("a.disease") == F.col("b.disease")) \
  .filter(F.col("a.target") < F.col("b.target")) \
  .repartition(F.col('a.target')) \
  .groupBy(F.col("a.target"), F.col("b.target")).count() \
  .filter(F.col("count") > 1) \
  .count()

print (targetPairs)
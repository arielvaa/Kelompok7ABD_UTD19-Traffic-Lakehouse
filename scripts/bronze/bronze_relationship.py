from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("BronzeRelationship") \
    .getOrCreate()

traffic = spark.read.csv(
    "medallion/bronze/raw/utd19_u.csv",
    header=True,
    inferSchema=True
)

detectors = spark.read.csv(
    "medallion/bronze/raw/detectors_public.csv",
    header=True,
    inferSchema=True
)

links = spark.read.csv(
    "medallion/bronze/raw/links.csv",
    header=True,
    inferSchema=True
)

print("Traffic distinct detid:")
print(traffic.select("detid").distinct().count())

print("Detector distinct detid:")
print(detectors.select("detid").distinct().count())

print("Detector distinct linkid:")
print(detectors.select("linkid").distinct().count())

print("Links distinct linkid:")
print(links.select("linkid").distinct().count())

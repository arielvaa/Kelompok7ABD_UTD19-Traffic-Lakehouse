from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("DupCheck") \
    .getOrCreate()

detectors = spark.read.csv(
    "medallion/bronze/raw/detectors_public.csv",
    header=True,
    inferSchema=True
)

dup = (
    detectors
    .groupBy("detid")
    .count()
    .filter("count > 1")
)

print(
    "Jumlah detid duplikat:"
)

print(
    dup.count()
)

dup.show(20, False)

spark.stop()

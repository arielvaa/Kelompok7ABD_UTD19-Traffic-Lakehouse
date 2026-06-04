import time

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("ReadParquet")
    .getOrCreate()
)

start = time.time()

df = spark.read.parquet(
    "medallion/silver/parquet/traffic_enriched"
)

rows = df.count()

end = time.time()

print("Rows:", rows)
print("Read Time:", end - start)

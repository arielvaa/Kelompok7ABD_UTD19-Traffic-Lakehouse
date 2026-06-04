import time

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("FilterParquet")
    .getOrCreate()
)

df = spark.read.parquet(
    "medallion/silver/parquet/traffic_enriched"
)

start = time.time()

count = (
    df.filter(df.city == "london")
    .count()
)

end = time.time()

print("Rows:", count)
print("Filter Time:", end - start)

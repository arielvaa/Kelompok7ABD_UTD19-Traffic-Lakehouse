import time

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("AggParquet")
    .getOrCreate()
)

df = spark.read.parquet(
    "medallion/silver/parquet/traffic_enriched"
)

start = time.time()

result = (
    df.groupBy("city")
    .avg("flow")
)

result.show()

end = time.time()

print("Aggregation Time:", end - start)

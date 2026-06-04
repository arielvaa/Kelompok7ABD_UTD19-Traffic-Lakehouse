import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg

spark = (
    SparkSession.builder
    .appName("GoldCityDailyParquet")
    .getOrCreate()
)

start = time.time()

silver = spark.read.parquet(
    "medallion/silver/parquet/traffic_enriched"
)

gold = (
    silver
    .groupBy(
        "city",
        "day"
    )
    .agg(
        avg("flow").alias("avg_flow"),
        avg("speed").alias("avg_speed"),
        avg("occ").alias("avg_occ")
    )
)

gold.write.mode("overwrite").parquet(
    "medallion/gold/parquet/city_daily"
)

print("Rows:", gold.count())
print("Time:", time.time() - start)

spark.stop()

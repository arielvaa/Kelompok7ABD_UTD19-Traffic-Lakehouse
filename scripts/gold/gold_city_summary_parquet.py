import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg,countDistinct

spark = (
    SparkSession.builder
    .appName("GoldCitySummaryParquet")
    .getOrCreate()
)

start = time.time()

silver = spark.read.parquet(
    "medallion/silver/parquet/traffic_enriched"
)

gold = (
    silver
    .groupBy("city")
    .agg(
        avg("flow").alias("avg_flow"),
        avg("speed").alias("avg_speed"),
        avg("occ").alias("avg_occ"),
        countDistinct("detid").alias("detector_count")
    )
)

gold.write.mode("overwrite").parquet(
    "medallion/gold/parquet/city_summary"
)

gold.show(50, False)

print("Rows:", gold.count())
print("Time:", time.time() - start)

spark.stop()

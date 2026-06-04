import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg,count

spark = (
    SparkSession.builder
    .appName("GoldRoadAnalysisParquet")
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
        "fclass"
    )
    .agg(
        avg("flow").alias("avg_flow"),
        avg("speed").alias("avg_speed"),
        count("*").alias("records")
    )
)

gold.write.mode("overwrite").parquet(
    "medallion/gold/parquet/road_analysis"
)

gold.show(100, False)

print("Rows:", gold.count())
print("Time:", time.time() - start)

spark.stop()

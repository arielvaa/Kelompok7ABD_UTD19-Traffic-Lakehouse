import time

from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .appName("ReadDelta")
    .config(
        "spark.sql.extensions",
        "io.delta.sql.DeltaSparkSessionExtension"
    )
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    )
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()

start = time.time()

df = (
    spark.read
    .format("delta")
    .load(
        "medallion/silver/delta/traffic_enriched"
    )
)

print("Rows:", df.count())

end = time.time()

print("Read Time:", end - start)

spark.stop()

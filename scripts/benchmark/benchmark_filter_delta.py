import time

from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .appName("FilterDelta")
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

df = (
    spark.read
    .format("delta")
    .load(
        "medallion/silver/delta/traffic_enriched"
    )
)

start = time.time()

result = (
    df.filter(
        df.flow > 300
    )
)

print("Rows:", result.count())

end = time.time()

print("Filter Time:", end - start)

spark.stop()

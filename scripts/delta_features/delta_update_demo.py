from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .appName("DeltaUpdate")
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
        "medallion/gold/delta/city_summary"
    )
)

updated = (
    df.withColumn(
        "congestion_index",
        col("avg_flow") / col("avg_speed")
    )
)

(
    updated.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(
        "medallion/gold/delta/city_summary"
    )
)

print("Update Success")

spark.stop()

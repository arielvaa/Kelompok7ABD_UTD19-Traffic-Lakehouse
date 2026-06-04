from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .appName("TimeTravel")
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

print("=" * 50)
print("VERSION 0")
print("=" * 50)

old_df = (
    spark.read
    .format("delta")
    .option("versionAsOf", 0)
    .load(
        "medallion/gold/delta/city_summary"
    )
)

old_df.printSchema()

print("=" * 50)
print("LATEST VERSION")
print("=" * 50)

new_df = (
    spark.read
    .format("delta")
    .load(
        "medallion/gold/delta/city_summary"
    )
)

new_df.printSchema()

spark.stop()

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg,countDistinct
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .appName("GoldCitySummaryDelta")
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

silver = spark.read.format("delta").load(
    "medallion/silver/delta/traffic_enriched"
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

(
    gold.write
    .format("delta")
    .mode("overwrite")
    .save(
        "medallion/gold/delta/city_summary"
    )
)

print("Rows:", gold.count())

spark.stop()

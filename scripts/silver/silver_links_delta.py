from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .appName("SilverLinksDelta")
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

links = spark.read.csv(
    "medallion/bronze/raw/links.csv",
    header=True,
    inferSchema=True
)

(
    links
    .write
    .format("delta")
    .mode("overwrite")
    .save(
        "medallion/silver/delta/links"
    )
)

spark.stop()

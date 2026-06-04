from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("SilverLinksParquet")
    .getOrCreate()
)

links = spark.read.csv(
    "medallion/bronze/raw/links.csv",
    header=True,
    inferSchema=True
)

(
    links
    .write
    .mode("overwrite")
    .parquet(
        "medallion/silver/parquet/links"
    )
)

spark.stop()

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SchemaCheck") \
    .getOrCreate()

df = spark.read.parquet(
    "medallion/silver/parquet/traffic_enriched"
)

df.printSchema()

spark.stop()

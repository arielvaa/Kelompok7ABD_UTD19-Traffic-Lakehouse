from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ValidateParquet") \
    .getOrCreate()

df = spark.read.parquet(
    "medallion/silver/parquet/traffic_enriched"
)

print("Parquet Rows:")
print(df.count())

spark.stop()

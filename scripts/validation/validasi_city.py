from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("CityCheck") \
    .getOrCreate()

df = spark.read.parquet(
    "medallion/silver/parquet/traffic_enriched"
)

print(
    "Jumlah Kota:"
)

print(
    df.select("city")
    .distinct()
    .count()
)

spark.stop()

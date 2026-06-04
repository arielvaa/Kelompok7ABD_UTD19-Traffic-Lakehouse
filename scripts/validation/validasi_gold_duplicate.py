from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("GoldDuplicateValidation")
    .getOrCreate()
)

print("="*60)
print("CITY SUMMARY")
print("="*60)

city_summary = spark.read.parquet(
    "medallion/gold/parquet/city_summary"
)

(
    city_summary
    .groupBy("city")
    .count()
    .filter("count > 1")
    .show()
)

print("="*60)
print("CITY DAILY")
print("="*60)

city_daily = spark.read.parquet(
    "medallion/gold/parquet/city_daily"
)

(
    city_daily
    .groupBy("city","day")
    .count()
    .filter("count > 1")
    .show()
)

spark.stop()

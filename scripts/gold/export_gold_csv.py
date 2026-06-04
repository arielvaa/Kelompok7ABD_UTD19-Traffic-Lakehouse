from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("ExportGoldCSV")
    .getOrCreate()
)

# Read Gold Tables
city_summary = spark.read.parquet(
    "medallion/gold/parquet/city_summary"
)

city_daily = spark.read.parquet(
    "medallion/gold/parquet/city_daily"
)

road_analysis = spark.read.parquet(
    "medallion/gold/parquet/road_analysis"
)

# Export CSV
city_summary.coalesce(1) \
    .write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("gold_csv/city_summary")

city_daily.coalesce(1) \
    .write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("gold_csv/city_daily")

road_analysis.coalesce(1) \
    .write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("gold_csv/road_analysis")

spark.stop()

print("Export selesai!")

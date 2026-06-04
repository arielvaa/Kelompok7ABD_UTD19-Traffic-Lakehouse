from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("GoldLogicValidation")
    .getOrCreate()
)

city_summary = spark.read.parquet(
    "medallion/gold/parquet/city_summary"
)

print("\nTOP 10 FLOW")

city_summary.orderBy(
    city_summary.avg_flow.desc()
).show(10, False)

print("\nTOP 10 SPEED")

city_summary.orderBy(
    city_summary.avg_speed.desc()
).show(10, False)

spark.stop()

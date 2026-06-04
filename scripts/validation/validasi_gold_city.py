from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("GoldCityValidation")
    .getOrCreate()
)

df = spark.read.parquet(
    "medallion/gold/parquet/city_summary"
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

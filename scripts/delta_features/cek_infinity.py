from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.getOrCreate()

df = spark.read.parquet(
    "medallion/gold/parquet/city_summary"
)

df.filter(
    col("avg_occ") == float("inf")
).show(50, False)

spark.stop()

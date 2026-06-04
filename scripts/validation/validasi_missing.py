from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("MissingCheck") \
    .getOrCreate()

df = spark.read.parquet(
    "medallion/silver/parquet/traffic_enriched"
)

total = df.count()

print("Total Rows:", total)

for c in [
    "detid",
    "linkid",
    "road",
    "fclass",
    "lanes"
]:
    miss = df.filter(
        col(c).isNull()
    ).count()

    print(
        f"{c}: {miss}"
    )

spark.stop()

import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast

spark = (
    SparkSession.builder
    .appName("SilverParquet")
    .getOrCreate()
)

start = time.time()

print("Loading traffic data...")

traffic = spark.read.csv(
    "medallion/bronze/raw/utd19_u.csv",
    header=True,
    inferSchema=True
)

print("Loading detector data...")

detectors = spark.read.csv(
    "medallion/bronze/raw/detectors_public.csv",
    header=True,
    inferSchema=True
)

print("Joining traffic + detectors...")

silver = (
    traffic
    .join(
        broadcast(detectors),
        on="detid",
        how="left"
    )
)

print("Schema:")

silver.printSchema()

print("Writing Parquet...")

(
    silver
    .repartition(8)
    .write
    .mode("overwrite")
    .parquet(
        "medallion/silver/parquet/traffic_enriched"
    )
)

end = time.time()

print(f"\nWrite Time: {end - start:.2f} seconds")

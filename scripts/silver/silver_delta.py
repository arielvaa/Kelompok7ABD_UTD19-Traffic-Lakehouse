import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .appName("SilverDelta")

    # Delta Lake
    .config(
        "spark.sql.extensions",
        "io.delta.sql.DeltaSparkSessionExtension"
    )
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    )

    # Optimasi VM 2 Core / 8 GB
    .config(
        "spark.sql.shuffle.partitions",
        "2"
    )
    .config(
        "spark.default.parallelism",
        "2"
    )
    .config(
        "spark.sql.adaptive.enabled",
        "true"
    )
    .config(
        "spark.sql.adaptive.coalescePartitions.enabled",
        "true"
    )

    # Memory
    .config(
        "spark.executor.memory",
        "4g"
    )
    .config(
        "spark.driver.memory",
        "2g"
    )

    # Kompresi
    .config(
        "spark.sql.parquet.compression.codec",
        "snappy"
    )
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()

start = time.time()

print("=" * 60)
print("READ TRAFFIC CSV")
print("=" * 60)

traffic = spark.read.csv(
    "medallion/bronze/raw/utd19_u.csv",
    header=True,
    inferSchema=True
)

print("Traffic loaded")

print("=" * 60)
print("READ DETECTORS CSV")
print("=" * 60)

detectors = spark.read.csv(
    "medallion/bronze/raw/detectors_public.csv",
    header=True,
    inferSchema=True
)

print("Detectors loaded")

print("=" * 60)
print("JOIN TRAFFIC + DETECTORS")
print("=" * 60)

silver = (
    traffic
    .join(
        broadcast(detectors),
        on="detid",
        how="left"
    )
)

print("Join complete")

print("=" * 60)
print("WRITE DELTA")
print("=" * 60)

(
    silver
    .repartition(2)
    .write
    .format("delta")
    .mode("overwrite")
    .save(
        "medallion/silver/delta/traffic_enriched"
    )
)

end = time.time()

print("=" * 60)
print("DELTA WRITE SUCCESS")
print("=" * 60)

print(f"Write Time : {end - start:.2f} seconds")

spark.stop()

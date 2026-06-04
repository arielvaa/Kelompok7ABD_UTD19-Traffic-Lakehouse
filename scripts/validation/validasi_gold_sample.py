from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("GoldSampleValidation")
    .getOrCreate()
)

tables = [
    "city_summary",
    "city_daily",
    "road_analysis"
]

for table in tables:

    print("\n" + "="*60)
    print(f"SAMPLE DATA : {table}")
    print("="*60)

    df = spark.read.parquet(
        f"medallion/gold/parquet/{table}"
    )

    df.show(10, False)

spark.stop()

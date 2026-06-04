from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("GoldSchemaValidation")
    .getOrCreate()
)

tables = [
    "city_summary",
    "city_daily",
    "road_analysis"
]

for table in tables:

    print("\n" + "="*60)
    print(f"SCHEMA : {table}")
    print("="*60)

    df = spark.read.parquet(
        f"medallion/gold/parquet/{table}"
    )

    df.printSchema()

spark.stop()

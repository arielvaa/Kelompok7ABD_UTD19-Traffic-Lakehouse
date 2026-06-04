from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("GoldValidation") \
    .getOrCreate()

tables = [
    "city_summary",
    "city_daily",
    "road_analysis"
]

for t in tables:

    print("\n" + "="*50)
    print(t)
    print("="*50)

    df = spark.read.parquet(
        f"medallion/gold/parquet/{t}"
    )

    print("Rows:", df.count())
    print("Columns:", len(df.columns))

spark.stop()

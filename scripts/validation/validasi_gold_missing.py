from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("GoldMissingValidation")
    .getOrCreate()
)

tables = [
    "city_summary",
    "city_daily",
    "road_analysis"
]

for table in tables:

    print("\n" + "="*60)
    print(f"MISSING VALUE : {table}")
    print("="*60)

    df = spark.read.parquet(
        f"medallion/gold/parquet/{table}"
    )

    total = df.count()

    print("Rows :", total)

    for c in df.columns:

        miss = df.filter(
            col(c).isNull()
        ).count()

        print(f"{c}: {miss}")

spark.stop()

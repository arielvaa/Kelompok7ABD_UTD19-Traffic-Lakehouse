from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("BronzeProfile") \
    .getOrCreate()

files = {
    "traffic": "medallion/bronze/raw/utd19_u.csv",
    "detectors": "medallion/bronze/raw/detectors_public.csv",
    "links": "medallion/bronze/raw/links.csv"
}

for name, path in files.items():

    print(f"\n==== {name.upper()} ====")

    df = spark.read.csv(
        path,
        header=True,
        inferSchema=True
    )

    print("Rows:", df.count())
    print("Columns:", len(df.columns))

    for c in df.columns:
        missing = df.filter(col(c).isNull()).count()
        print(f"{c}: {missing}")

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when

spark = SparkSession.builder \
    .appName("DataQuality") \
    .getOrCreate()

df = spark.read.csv(
    "medallion/bronze/raw/utd19_u.csv",
    header=True,
    inferSchema=True
)

print("Jumlah baris:")
print(df.count())

print("\nMissing value per kolom:")

for c in df.columns:
    n = df.filter(col(c).isNull()).count()
    print(c, n)

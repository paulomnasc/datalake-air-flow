from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_date
import boto3


# Inicializa a sessão Spark com suporte ao Delta Lake
spark = SparkSession.builder \
    .appName("IngestaoDeltaClientes") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Configurações para acessar o MinIO via S3
spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", "admin")
spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "admin123")
spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://minio:9000")
spark._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
spark._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

# Leitura de dados brutos (exemplo: CSV no MinIO)
df = spark.read.option("header", True).csv("s3a://raw/clientes/clientes.csv")

# Enriquecimento com coluna de partição
df = df.withColumn("partition_date", current_date())

# Escrita em Delta Lake com particionamento por data
df.write.format("delta") \
    .mode("append") \
    .partitionBy("partition_date") \
    .save("s3a://delta/clientes")

spark.stop()
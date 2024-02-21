from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("MongoDB to PySpark") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/my_graph_database.edges") \
    .getOrCreate()

# Read data from MongoDB into a DataFrame
df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()

# Show the DataFrame
df.show()

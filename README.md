# Data-Extraction-from-Youtube-and-Data-Pipeline-using-AWS-Glue
Extracted data from Dhruv Rathee Youtube Channel using Youtube API and created an ETL Job using AWS Glue to write the dataset in desired S3 Bucket


Using the code {https://github.com/Abh1shekkkM/Data-Extraction-from-Youtube-and-Data-Pipeline-using-AWS-Glue/blob/main/youtube_etl_project.py},
I extracted the data from a popular Youtuber channel which contains data points like his video title, comment text, like counts etc.

This dataset is then stored on a S3 bucket which is then used as a source for ETL Job in AWS Glue to load into another bucket.

This ETL job in real world is used for multiple business cases like Data Compliance, Staging & Production difference in buckets, Data Validation, data transformation etc.

ETL Job Script excerpt from Glue:

    from pyspark.context import SparkContext
    from awsglue.context import GlueContext
    from pyspark.sql import SparkSession
    
    # Create a Spark context and Glue context
    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    
    # Read CSV file from source S3 bucket
    source_df = spark.read.csv("s3://etl-youtube/youtube_data.csv", header=True, inferSchema=True)
    
    # Write CSV file to destination S3 bucket
    source_df.write.csv("s3://etl-youtube-destination/youtube_data_output.csv", mode="overwrite", header=True)

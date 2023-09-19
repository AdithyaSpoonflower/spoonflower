import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node S3 bucket
S3bucket_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="catalogue-magnolia-datahub-prod",
    table_name="raw_direct_order_ledger",
    transformation_ctx="S3bucket_node1",
)

# Script generated for node Change Schema
ChangeSchema_node2 = ApplyMapping.apply(
    frame=S3bucket_node1,
    mappings=[
        ("id", "int", "id", "int"),
        ("order_id", "int", "order_id", "int"),
        ("customer_id", "int", "customer_id", "int"),
        ("customer_email", "string", "customer_email", "string"),
        ("sf_user_id", "int", "sf_user_id", "int"),
        ("sf_order_id", "int", "sf_order_id", "int"),
        ("event_type", "string", "event_type", "string"),
        ("metadata", "string", "metadata", "string"),
        ("created_at", "timestamp", "created_at", "timestamp"),
    ],
    transformation_ctx="ChangeSchema_node2",
)

# Script generated for node Amazon Redshift
AmazonRedshift_node3 = glueContext.write_dynamic_frame.from_options(
    frame=ChangeSchema_node2,
    connection_type="redshift",
    connection_options={
        "redshiftTmpDir": "s3://aws-glue-assets-773459762593-us-east-1/temporary/",
        "useConnectionProperties": "true",
        "dbtable": "magnolia.raw_direct_order_ledger",
        "connectionName": "glueconnection-magnolia-dwh-prod",
        "preactions": "CREATE TABLE IF NOT EXISTS magnolia.raw_direct_order_ledger (id INTEGER, order_id INTEGER, customer_id INTEGER, customer_email VARCHAR, sf_user_id INTEGER, sf_order_id INTEGER, event_type VARCHAR, metadata VARCHAR, created_at TIMESTAMP);",
    },
    transformation_ctx="AmazonRedshift_node3",
)

job.commit()

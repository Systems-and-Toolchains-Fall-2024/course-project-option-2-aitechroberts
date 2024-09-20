import os
import zipfile
from google.cloud import storage
from kaggle.api.kaggle_api_extended import KaggleApi
from pyspark.sql import SparkSession
from google.cloud import dataproc_v1

# Function to submit a PySpark job to Dataproc
def submit_pyspark_job(cluster_name, project_id, region, gcs_bucket, input_path, output_path, database, username, password):
    job_client = dataproc_v1.JobControllerClient(
        client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
    )
    
    # PySpark job definition
    job = {
        "placement": {"cluster_name": cluster_name},
        "pyspark_job": {
            "main_python_file_uri": f"gs://{gcs_bucket}/pyspark_job.py",
            "args": [input_path, output_path, database, username, password],
        },
    }
    
    # Submit job to Dataproc
    operation = job_client.submit_job_as_operation(
        request={"project_id": project_id, "region": region, "job": job}
    )
    
    # Wait for the job to complete
    response = operation.result(timeout=600)
    return response

# Function to download Kaggle dataset
def download_kaggle_dataset(dataset: str, download_path: str):
    api = KaggleApi()
    api.authenticate()
    
    # Download dataset as zip file
    api.dataset_download_files(dataset, path=download_path, unzip=False)
    zip_file = os.path.join(download_path, dataset.split("/")[-1] + ".zip")
    
    return zip_file

# Function to upload a file to Google Cloud Storage
def upload_to_gcs(bucket_name: str, source_file: str, destination_blob: str):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    
    # Upload the file
    blob.upload_from_filename(source_file)

# PySpark job for processing Kaggle dataset
def process_kaggle_to_gcs_with_spark(kaggle_dataset: str, gcs_bucket: str, gcs_blob: str):
    # Initialize Spark session
    spark = SparkSession.builder.appName("KaggleDatasetUpload").getOrCreate()
    
    # Create a temporary directory to download the dataset
    download_path = "temp_download"
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    # Step 1: Download dataset from Kaggle
    zip_file = download_kaggle_dataset(kaggle_dataset, download_path)
    
    # Step 2: Unzip the dataset
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(download_path)
    
    # Track the files extracted
    files_to_upload = [os.path.join(download_path, f) for f in os.listdir(download_path) if f.endswith(".csv")]
    
    # Upload files to GCS using PySpark (for parallelization)
    rdd = spark.sparkContext.parallelize(files_to_upload)
    
    def upload_file(file_path):
        file_name = os.path.basename(file_path)
        upload_to_gcs(gcs_bucket, file_path, gcs_blob + "/" + file_name)
    
    # Perform the upload in parallel using PySpark
    rdd.foreach(upload_file)
    
    # Cleanup local files
    for file in files_to_upload:
        os.remove(file)
    os.remove(zip_file)

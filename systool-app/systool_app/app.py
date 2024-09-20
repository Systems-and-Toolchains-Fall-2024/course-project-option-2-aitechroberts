import streamlit as st
from pyspark_jobs import submit_pyspark_job

def main():
    st.title("Kaggle Dataset to Google Cloud Storage with PySpark")

    # Input fields for Kaggle dataset and GCS paths
    kaggle_dataset = st.text_input("Enter Kaggle Dataset (e.g., zillow/zecon):")
    gcs_bucket = st.text_input("Enter GCS Bucket Name:")
    gcs_blob = st.text_input("Enter GCS Blob Path:")
    
    if st.button("Download Dataset and Upload to GCS"):
        if kaggle_dataset and gcs_bucket and gcs_blob:
            try:
                st.write("Submitting PySpark job to Dataproc...")
                
                # Submit the PySpark job to Dataproc
                response = submit_pyspark_job(
                    cluster_name="my-cluster",
                    project_id="your-project-id",
                    region="us-central1",
                    gcs_bucket=gcs_bucket,
                    input_path=f"gs://{gcs_bucket}/input-file",
                    output_path=f"gs://{gcs_bucket}/output-folder",
                    database="postgres",
                    username="postgres",
                    password="pg_password"
                )
                
                st.success("Dataproc job submitted successfully.")
                st.write(f"Job ID: {response.job_uuid}")

                # Extend here to monitor the job status if needed
                job_status = "PENDING"  # Example: Set to track job status
                st.write(f"Current job status: {job_status}")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please fill in all fields before proceeding.")

if __name__ == "__main__":
    main()

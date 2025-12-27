import requests
import time
import logging
import io
import os
from datetime import datetime, UTC
from google.cloud import storage

# ===============================
# Configuration
# ===============================

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
BUCKET_NAME = f"{PROJECT_ID}-data-bucket"

GCS_DATA_FOLDER = "dataset/trips/"
GCS_LOG_FOLDER = "from-git/logs/"

START_YEAR = 2023
CURRENT_YEAR = datetime.now(UTC).year

REQUEST_TIMEOUT = 60  # seconds
SLEEP_SECONDS = 1

# ===============================
# GCS Client
# ===============================

storage_client = storage.Client()

# ===============================
# Logging configuration
# ===============================

log_stream = io.StringIO()
logging.basicConfig(
    stream=log_stream,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ===============================
# Utility functions
# ===============================

def file_exists_in_gcs(bucket_name: str, gcs_path: str) -> bool:
    """Check if a file already exists in GCS."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)
    return blob.exists()

def upload_bytes_to_gcs(bucket_name: str, gcs_path: str, content: bytes):
    """Upload binary content to GCS."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)
    blob.upload_from_string(content)
    logging.info(f"Uploaded file to gs://{bucket_name}/{gcs_path}")

def upload_log_to_gcs():
    """Upload execution logs to GCS."""
    log_filename = (
        f"{GCS_LOG_FOLDER}"
        f"extract_log_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.log"
    )
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(log_filename)
    blob.upload_from_string(log_stream.getvalue())
    logging.info(f"Log file uploaded to gs://{BUCKET_NAME}/{log_filename}")

# ===============================
# Main extraction function
# ===============================

def download_historical_taxi_data():
    """
    Download NYC Yellow Taxi PARQUET files from 2023 to current year
    and upload them directly to Google Cloud Storage.
    """

    try:
        for year in range(START_YEAR, CURRENT_YEAR + 1):
            for month in range(1, 13):

                file_name = f"yellow_tripdata_{year}-{month:02d}.parquet"
                gcs_path = f"{GCS_DATA_FOLDER}{file_name}"
                download_url = (
                    f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file_name}"
                )

                if file_exists_in_gcs(BUCKET_NAME, gcs_path):
                    logging.info(f"{file_name} already exists in GCS. Skipping.")
                    continue

                logging.info(f"Downloading {file_name}...")

                try:
                    response = requests.get(
                        download_url,
                        stream=True,
                        timeout=REQUEST_TIMEOUT
                    )

                    if response.status_code == 200:
                        upload_bytes_to_gcs(
                            BUCKET_NAME,
                            gcs_path,
                            response.content
                        )

                    elif response.status_code == 404:
                        logging.warning(
                            f"{file_name} not found on source. Skipping."
                        )

                    else:
                        logging.error(
                            f"Failed to download {file_name}. "
                            f"HTTP {response.status_code}"
                        )

                except requests.RequestException as e:
                    logging.error(
                        f"HTTP error while downloading {file_name}: {str(e)}"
                    )

                time.sleep(SLEEP_SECONDS)

        logging.info("Download process completed successfully.")

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")

    finally:
        upload_log_to_gcs()

# ===============================
# Entry point
# ===============================

if __name__ == "__main__":
    logging.info(
        f"Starting NYC Yellow Taxi data download - "
        f"Start year: {START_YEAR}"
    )
    download_historical_taxi_data()

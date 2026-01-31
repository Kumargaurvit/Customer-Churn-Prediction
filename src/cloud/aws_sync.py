import os
import sys
from src.exception.exception import CustomerChurnException
from src.logging.logger import logging

class AWSSync:
    def __init__(self):
        pass

    def sync_to_s3(self, folder, aws_bucket_url):
        try:
            logging.info("Syncing files to AWS S3 Bucket")
            command = f"aws s3 sync {folder} {aws_bucket_url}"
            os.system(command)
        except Exception as e:
            raise CustomerChurnException(e,sys)
    
    def retrieve_from_s3(self, folder, aws_bucket_url):
        try:
            logging.info("Retrieving files from AWS S3 Bucket")
            command = f"aws s3 sync {aws_bucket_url} {folder}"
        except Exception as e:
            raise CustomerChurnException(e,sys)
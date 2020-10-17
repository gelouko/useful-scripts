import logging
from botocore.exceptions import ClientError
from modules.resource_manager import ResourceManager


class S3(ResourceManager):
    def __init__(self, client):
        self.client = client

    def list_resources(self):
        logging.info('Listing S3 buckets...')
        return self.client.list_buckets()['Buckets']

    def get_tags(self, bucket):
        logging.info('Listing bucket tags...')
        try:
            return self.client.get_bucket_tagging(
                Bucket=bucket['Name']
            )['TagSet']
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchTagSet':
                logging.info('bucket contains no tags.')
                return []

            raise e

    def put_tags(self, bucket, tags):
        logging.info('Putting bucket tags...')
        return self.client.put_bucket_tagging(
            Bucket=bucket['Name'],
            Tagging={'TagSet': tags}
        )

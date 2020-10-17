class ResourceManager:
    def list_resources(self):
        """Uses AWS CLI to list all resources from that module

        Example:
        List all S3 buckets:
        self.client.list_buckets()['Bucket']
        """
        pass

    def get_tags(self, resource):
        """Uses AWS CLI to fetch a list of tags of a resource

        Example:
        Fetch all tags from an S3 bucket:
        self.client.get_bucket_tagging(Bucket='MyBucket')['TagSet']
        """
        pass

    def put_tags(self, resource, tags):
        """Uses AWS CLI to write a list of tags to a resource

        Example:
        Write all tags to an S3 bucket:
        self.client.put_bucket_tagging(
            Bucket='MyBucket',
            Tagging={'TagSet': tags}
        )
        """
        pass

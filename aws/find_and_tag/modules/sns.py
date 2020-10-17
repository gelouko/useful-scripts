import logging
from modules.resource_manager import ResourceManager


class SNS(ResourceManager):
    def __init__(self, client):
        self.client = client

    def list_resources(self):
        logging.info('Listing SNS topics...')
        return self.client.list_topics()['Topics']

    def get_tags(self, topic):
        logging.info('Listing topic tags...')
        return self.client.list_tags_for_resource(
            ResourceArn=topic['TopicArn']
        )['Tags']

    def put_tags(self, topic, tags):
        logging.info('Putting topic tags...')
        return self.client.tag_resource(
            ResourceArn=topic['TopicArn'],
            Tags=tags
        )

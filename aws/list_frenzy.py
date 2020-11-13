# Just listing some resources with AWS's pagination
# while logging the API Calls from AWS

import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def list_lambdas():
    client = boto3.client('lambda')

    paginator = client.get_paginator('list_functions')
    response_iterator = paginator.paginate(
        PaginationConfig={
            'PageSize': 50
        }
    )

    for response in response_iterator:
        for function in response['Functions']:
            print(function['FunctionName'])


def list_queues():
    client = boto3.client('sqs')

    paginator = client.get_paginator('list_queues')

    request_iterator = paginator.paginate(
        PaginationConfig={
            'PageSize': 50
        }
    )

    for page in request_iterator:
        for queue_url in page['QueueUrls']:
            print(queue_url)


def list_topics():
    client = boto3.client('sns')

    paginator = client.get_paginator('list_topics')

    # The SNS API does not support PageSize
    request_iterator = paginator.paginate()

    for page in request_iterator:
        for item in page['Topics']:
            print(item['TopicArn'])


def list_instances():
    client = boto3.client('ec2')

    paginator = client.get_paginator('describe_instances')

    request_iterator = paginator.paginate(
        PaginationConfig={
            'PageSize': 50
        }
    )

    for page in request_iterator:
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                print(instance['InstanceId'])


def lambda_handler(event, context):
    list_lambdas()
    list_queues()
    list_topics()
    list_instances()

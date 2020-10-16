import boto3
import re
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

########################################################################
# Example request (using default roleToAssume and roleSessionName):
#
# {
#     'region': 'sa-east-1',
#     's3': {
#         'nameExpressions': ['my-test-bucket-.*'],
#         'tags': [{
#             'Key': 'Tagged',
#             'Value': 'Me'
#         }]
#     },
#     'sns': {
#         'nameExpressions': ['.*-topic'],
#         'tags': [{
#             'Key': 'TagMy',
#             'Value': 'Topic'
#         }]
#     }
# }
########################################################################


default_config = {
    'roleToAssume': 'arn:aws:iam::{account_id}:role/CrossAccountRole',
    'roleSessionName': 'find-and-tag-script-execution',
    'region': 'us-east-1',
    's3': {
        'nameExpressions': [],
        'tags': []
    },
    'sns': {
        'nameExpressions': [],
        'tags': []
    }
}


def match_any_expression(value='', expressions=[]):
    """verifies if the input value matches any of the expressions using re

    Args:
        value (str, optional):
            [string to be tested against the expressions]. Defaults to ''.
        expressions (list, optional):
            [list of patterns (as strings) to test the value]. Defaults to [].
    """
    for expression in expressions:
        if re.match(expression, value):
            return True

    return False


def merge_distinct_tags(tag_list_a=[], tag_list_b=[]):
    """Returns a merge from both inputs, but choosing tag_list_b's tag values
    in case of equal keys

    Args:
        tag_list_a (list, optional): [List of tags]. Defaults to [].
        tag_list_b (list, optional): [List of tags]. Defaults to [].
    """
    tag_list_b_keys = map(lambda tag: tag['Key'], tag_list_b)
    merge = list(tag_list_b)

    for tag in tag_list_a:
        if tag['Key'] not in tag_list_b_keys:
            merge.append(tag)

    return merge


def lambda_handler(event, context):
    """Finds and tags some resources based on custom resource filters.
    Depending on your flexibility, you could use Cloud Custodian to do
    the same thing in an easier way. It assumes a role for execution

    List of necessary permissions for the Lambda execution role:
        sts:assumeRole (for the role to be assumed)
        [TODO]

    List of permissions for the assumed role:
        s3:listBuckets
        [TODO]

    Args:
        event (object): [the function payload.]
        context (object): [the lambda context]
    """
    account_id = re.search(
        'arn:aws:lambda:(.*):(.*):(.*):(.*)',
        context.invoked_function_arn
    ).group(2)
    default_config['roleToAssume'] = re.sub(
        '\\{account_id\\}',
        account_id,
        default_config['roleToAssume']
    )
    config = dict(default_config, **event)

    sts_client = boto3.client('sts')
    credentials = sts_client.assume_role(
        RoleArn=config['roleToAssume'],
        RoleSessionName=config['roleSessionName']
    )['Credentials']
    session = boto3.session.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name=config['region']
    )

    s3_client = session.client('s3')
    bucket_list = s3_client.list_buckets()['Buckets']
    selected_buckets = filter(
        lambda bucket: match_any_expression(
            bucket['Name'],
            config['s3']['nameExpressions']
        ),
        bucket_list
    )

    for selected_bucket in selected_buckets:
        current_tags = s3_client.get_bucket_tagging(
            Bucket=selected_bucket['Name']
        )['TagSet']

        logging.info('Putting tags into bucket %s', selected_bucket['Name'])
        s3_client.put_bucket_tagging(
            Bucket=selected_bucket['Name'],
            Tagging={
                'TagSet': merge_distinct_tags(
                    current_tags,
                    config['s3']['tags']
                )
            }
        )

    sns_client = session.client('sns')
    topic_list = sns_client.list_topics()['Topics']

    selected_topics = filter(
        lambda topic: match_any_expression(
            re.search(
                'arn:aws:sns:(.+):(\\d+):(.*)',
                topic['TopicArn']
            ).group(3),
            config['sns']['nameExpressions']
        ),
        topic_list
    )

    for selected_topic in selected_topics:
        logging.info('Putting tags into topic %s', selected_topic['TopicArn'])
        sns_client.tag_resource(
            ResourceArn=selected_topic['TopicArn'],
            Tags=config['sns']['tags']
        )

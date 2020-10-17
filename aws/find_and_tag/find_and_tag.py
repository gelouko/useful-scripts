from utils import match_any_expression, merge_distinct_tags
import boto3
import importlib
import logging
import structured_logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
structured_logging.init()


########################################################################
# Example Request:
#
# {
#     "resources": {
#         "s3": {
#             "nameExpressions": ["my-test-bucket-.*"],
#             "filterAttribute": "Name",
#             "tags": [{
#                 "Key": "Tagged",
#                 "Value": "Me"
#             }]
#         },
#         "sns": {
#             "nameExpressions": [".*-topic"],
#             "filterAttribute": "TopicArn",
#             "tags": [{
#                 "Key": "TagMy",
#                 "Value": "Topic"
#             }]
#         }
#     }
# }
########################################################################


def validate_event(event):
    if 'resources' not in event or type(event['resources']) != dict:
        raise AssertionError('"resources" is required and is a dict')

    for resource_name, resource in event['resources'].items():
        if ('nameExpressions' not in resource
           or type(resource['nameExpressions']) != list
           or len(resource['nameExpressions']) == 0):
            raise AssertionError(
                '"resources.nameExpressions" is required ' +
                'and is a list (not empty)'
            )

        if ('filterAttribute' not in resource
           or type(resource['filterAttribute']) != str):
            raise AssertionError(
                '"resources.filterAttribute" is required and is a string'
            )

        if ('tags' not in resource
           or type(resource['tags']) != list):
            raise AssertionError('"resources.tags" is required and is a list')

        invalid_tags = list(filter(
            lambda tag:
                len(set(tag.keys()).intersection({'Key', 'Value'})) != 2,
            resource['tags']
        ))
        if len(invalid_tags) > 0:
            raise AssertionError(
                'each tag in "resources.tags" needs a ' +
                '"Key" and "Value" attribute'
            )


def lambda_handler(event, context):
    """Finds and tags some resources based on custom resource filters.
    Depending on your flexibility, you could use Cloud Custodian to do
    the same thing in an easier way. It assumes a role for execution

    Be aware that your lambda execution role will need list resources
    and get/put tags permissions

    Args:
        event (object): [the function payload.]
        context (object): [the lambda context]
    """
    validate_event(event)

    for resource_name, resource_config in event['resources'].items():
        resource_module = importlib.import_module('modules.' + resource_name)
        client = boto3.client(resource_name)
        resource_manager = getattr(
            resource_module,
            resource_name.upper()
        )(client)

        fetched_list = resource_manager.list_resources()

        selected_resources = filter(
            lambda resource: match_any_expression(
                resource[resource_config['filterAttribute']],
                resource_config['nameExpressions']
            ),
            fetched_list
        )

        for selected_resource in selected_resources:
            current_tags = resource_manager.get_tags(selected_resource)

            resource_manager.put_tags(
                selected_resource,
                merge_distinct_tags(current_tags, resource_config['tags'])
            )

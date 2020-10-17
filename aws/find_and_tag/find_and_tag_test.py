import unittest
from unittest.mock import patch, MagicMock
from tests.mocks.boto3 import client
import find_and_tag
import importlib


class TestFindAndTag(unittest.TestCase):

    def test_validation_resource(self):
        for given in [
            {},
            {'resources': []},
            {'resources': ''},
            {'resources': 1}
        ]:
            with self.assertRaisesRegex(
                AssertionError,
                '"resources" is required and is a dict'
            ):
                find_and_tag.lambda_handler(given, {})

    def test_validation_name_expressions(self):
        for given in [
            {},
            {'nameExpressions': {}},
            {'nameExpressions': ''},
            {'nameExpressions': 1},
            {'nameExpressions': []}
        ]:
            with self.assertRaisesRegex(
                AssertionError,
                '"resources.nameExpressions" is required ' +
                'and is a list \\(not empty\\)'
            ):
                find_and_tag.lambda_handler({'resources': {'s3': given}}, {})

    def test_validation_filter_attribute(self):
        for given in [
            {'nameExpressions': ['']},
            {'nameExpressions': [''], 'filterAttribute': {}},
            {'nameExpressions': [''], 'filterAttribute': []},
            {'nameExpressions': [''], 'filterAttribute': 1}
        ]:
            with self.assertRaisesRegex(
                AssertionError,
                '"resources.filterAttribute" is required and is a string'
            ):
                find_and_tag.lambda_handler({'resources': {'s3': given}}, {})

    def test_validation_tags(self):
        for given in [
            {'nameExpressions': [''], 'filterAttribute': ''},
            {'nameExpressions': [''], 'filterAttribute': '', 'tags': {}},
            {'nameExpressions': [''], 'filterAttribute': '', 'tags': ''},
            {'nameExpressions': [''], 'filterAttribute': '', 'tags': 1}
        ]:
            with self.assertRaisesRegex(
                AssertionError,
                '"resources.tags" is required and is a list'
            ):
                find_and_tag.lambda_handler({'resources': {'s3': given}}, {})

        for given in [
            {
                'nameExpressions': [''],
                'filterAttribute': '',
                'tags': [{'Key': 'a'}]
            },
            {
                'nameExpressions': [''],
                'filterAttribute': '',
                'tags': [{'Value': 'a'}]
            },
            {
                'nameExpressions': [''],
                'filterAttribute': '',
                'tags': [{'Key': 'a', 'Val': 'a'}]
            }
        ]:
            with self.assertRaisesRegex(
                AssertionError,
                'each tag in "resources.tags" needs a ' +
                '"Key" and "Value" attribute'
            ):
                find_and_tag.lambda_handler({'resources': {'s3': given}}, {})

    @patch('boto3.client')
    def test_valid_resource_input(self, client):
        event = {
            'resources': {
                's3': {
                    'nameExpressions': ['test-.*'],
                    'filterAttribute': 'Name',
                    'tags': [{
                        'Key': 'Tagged',
                        'Value': 'Me'
                    }]
                }
            }
        }
        mocked_bucket = {'Name': 'test-1'}

        s3_manager_mock = MagicMock()
        s3_manager_mock.list_resources = MagicMock(
            return_value=[mocked_bucket]
        )
        s3_manager_mock.get_tags = MagicMock()
        s3_manager_mock.put_tags = MagicMock()
        module_mock = MagicMock()
        module_mock.S3 = MagicMock(return_value=s3_manager_mock)

        with patch.object(importlib, 'import_module',
             return_value=module_mock) as import_module_mock:
            find_and_tag.lambda_handler(event, {})

        import_module_mock.assert_called_with('modules.s3')
        client.assert_called_once_with('s3')
        s3_manager_mock.list_resources.assert_called_once()
        s3_manager_mock.get_tags.assert_called_once_with(mocked_bucket)
        s3_manager_mock.put_tags.assert_called_once_with(
            mocked_bucket,
            event["resources"]["s3"]["tags"]
        )


if __name__ == '__main__':
    unittest.main()

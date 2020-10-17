# Find and Tag

This script finds a resource based on an attribute expression (like a regex for a name) and tags the found resources with the input tags.

The function is ready to work with AWS Lambda environments.

## Example

If you have the following buckets:
- my-test-bucket-tag-me
- production-bucket
- images-bucket


And you provide the input:

```json
{
    "resources": {
        "s3": {
            "nameExpressions": ["my-test-bucket-.*"],
            "filterAttribute": "Name",
            "tags": [{
                "Key": "Tagged",
                "Value": "Me"
            }]
        }
    }
}
```

Then the bucket `my-test-bucket-tag-me` will be tagged with `Tagged: Me`.

You might also add another resources to the list of resources.

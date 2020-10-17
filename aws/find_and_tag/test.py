import importlib


resp = importlib.import_module('modules.s3')

print(getattr(resp, 'S3')())

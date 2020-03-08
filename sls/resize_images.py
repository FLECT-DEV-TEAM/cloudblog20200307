try:
  import unzip_requirements
except ImportError:
  pass

import json, time, os
from contextlib import contextmanager
import boto3
from boto3 import Session
from botocore.config import Config
from boto3.dynamodb.conditions import Key, Attr

from PIL import Image
import MultiProcessUtil

print('Loading function...')
 
s3 = boto3.resource('s3')

def resize_images(params):
    bucket = params[0]
    src_key = params[1]
    dst_key = params[2]

    img_size = 224

    tmp_path = f'/tmp/{src_key}'
    print(f'Downloading {src_key} to {tmp_path}....')

    os.makedirs(os.path.dirname(tmp_path), exist_ok=True)
    s3.Bucket(bucket).download_file(src_key, tmp_path)  

    img = Image.open(tmp_path, 'r')      
    img = img.resize((224, 224), Image.LANCZOS)
    img.save(tmp_path)

    s3.Bucket(bucket).upload_file(tmp_path, dst_key)
    os.remove(tmp_path)

def resize(event, context):
    ## パラメータ取得
    bucket = ''
    keys    = ''
    print(event)
    try:
      body   = json.loads(event['body'])
    except Exception as e:
      print(e)
      body = event['body']
    bucket = body['bucket']
    keys    = body['keys']
    print(bucket, keys)
    params = [bucket]*len(keys), keys, 
    params = [[bucket, x, f'resized2/{x}'] for x in keys]
        
    result = MultiProcessUtil.manager(params, resize_images, 8)

    return {
        "statusCode": 200,
        "body": json.dumps({
          "res":'OK',
        }),
    }


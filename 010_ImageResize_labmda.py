# Ignore  the warnings
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

import boto3
import os, glob, json, time
import MultiProcessUtil

import urllib.request
from PIL import Image
from contextlib import contextmanager

from botocore.credentials import Credentials
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV4Auth

# ACCESS_KEY    = os.environ['ACCESS_KEY']
# ACCESS_SECRET = os.environ['ACCESS_SECRET']
# REGION        = os.environ['REGION']
# URL           = os.environ['URL']
# BUCKET        = os.environ['BUCKET']

config = {}

with open('config.sh') as f:
    lines = f.readlines()
    for line in lines:
        pair = line.strip().split('=')
        if len(pair) == 2:
            config[pair[0]] = pair[1]

ACCESS_KEY    = config['ACCESS_KEY']
ACCESS_SECRET = config['ACCESS_SECRET']
REGION        = config['REGION']
URL           = config['URL']
URL2          = config['URL2']
BUCKET        = config['BUCKET']


@contextmanager
def timer(name):
    t0 = time.time()
    yield
    print(f'[{name}] done in {time.time() - t0:.0f} s')


def request_api_gateway(params):
    method = params[0]
    url    = params[1]
    data   = params[2]
    awsreq = AWSRequest(method=method, url=url, data=data)
    credentials = Credentials(ACCESS_KEY, ACCESS_SECRET)
    
    body = '---'
    SigV4Auth(credentials, "execute-api", REGION).add_auth(awsreq)
    req = urllib.request.Request(awsreq.url, awsreq.data, method=awsreq.method, headers=awsreq.headers)
    with urllib.request.urlopen(req) as res:
        body = json.load(res)
    return body


def resize_client(bucket, keys):
    method = 'POST'
    url    = URL
    
    params = []
    for i, key in enumerate(keys):
        params.append([method, url, json.dumps({'bucket':bucket, 'key':key}).encode()])

    ress = MultiProcessUtil.manager(params, request_api_gateway, 300)
    return ress


if __name__ == '__main__':
    files = glob.glob('input/**/*.jpeg', recursive=True)
    print('Num of files: ',len(files))
    with timer("Lambda Resize"):
        res = resize_client(BUCKET, files)
    

# Lambda Performance Evaluation

## Install Prerequisit

### serverless framework
```
$ npm install -g serverless
$ serverless config credentials --provider aws --key “IAMユーザのアクセスキーID”  --secret “IAMユーザのシークレットアクセスキー”
```

besides this, you need to install docker to use serverless framework, if you have not installed docker.

### plugins
```
$ cd sls
$ serverless plugin install -n serverless-python-requirements
$ serverless plugin install -n serverless-prune-plugin
```

## Prepare Images
### Local drive
- store images to the input dir. 
- the extension of the image must be '.jpeg'
### S3
- store the same images with the same key as the path
- for example, if the path of the image on drive is "input/aaa/bbb.jpeg", the key on the S3 is "input/aaa/bbb.jpeg".

## Deploy Lambda
```
$ cd sls
$ serverless deploy

```

## Configure API Gateway

Change timeout to 29sec.

## Configure Lambda

Set the role to use cloudwatch and S3.


## Demo

See 
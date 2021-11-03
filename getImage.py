# coding=utf-8
import boto3, urllib.parse, json, base64
from botocore.exceptions import ClientError
dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client("s3")


def getImage(event, context):
    #Função GetImage, que recebe como parâmetro o s3objectkey e faz o download da imagem.

    bucket="serverless-challenge-dev-bucket"
    file_name = urllib.parse.unquote_plus(event["pathParameters"]["s3objectkey"])
    s3objectkey="uploads/{}".format(file_name) #Nos endpoints "uploads/" foi removido da {s3objectkey} para simplificar a rota
    
    try: 
        obj = s3_client.get_object(Bucket=bucket, Key=s3objectkey)
        file_content = obj["Body"].read()
    except ClientError as e:
        print ({
            "statusCode": 422,
            "body": json.dumps({"message": "Error '{}' fetching file '{}'".format(e,s3objectkey),}),
            "headers":{}
        })
        raise e
    else:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "image/jpeg",
                "Content-Disposition": "attachment; filename={}".format(file_name)
            },
            "body": base64.b64encode(file_content).decode('utf-8'),
            "isBase64Encoded": True
        }
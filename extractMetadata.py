# coding=utf-8
import boto3, urllib.parse, json, io
from botocore.exceptions import ClientError
from PIL import Image
dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client("s3")

def extractMetadata(event, context):
    # Função ExtractMetadata, que é é chamada quando um novo arquivo é carregado no S3. Ela
    # deverá extrair os metadados da imagem (dimensões, tamanho do arquivo) e armazenar no
    # DynamoDB.
    # XXX.: Metadata não inclui dimensões é necessário, utilizando PIL a imagem é carregada
    # para ler as dimensões
    
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")
     
    try:
        
        obj = s3_client.get_object(Bucket=bucket, Key=key)
    
        im = Image.open(io.BytesIO(obj["Body"].read()))
        im_width, im_height = im.size

        folder_filename = key.split("/")

        response = dynamodb_client.put_item(
            TableName="serverless-challenge-dev",
            Item={
                "folder": {"S": folder_filename[0]},
                "filename" : {"S": folder_filename[1]},
                "contentlength" : {"N": str(obj["ContentLength"])},
                "contenttype" : {"S": obj["ContentType"]},
                "dimension" : {"S": "{}x{}".format(im_width,im_height)}
            }
        )
    except ClientError as e:
        raise e
    else:
        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }  
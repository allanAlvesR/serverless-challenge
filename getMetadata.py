# coding=utf-8
import boto3, urllib.parse, json
dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client("s3")

def getMetadata(event, context):
    #Função GetMetadata, que recebe a requisição de um endpoint criado pelo AWS API Gateway.
    #Ela irá receber o parâmetro s3objectkey e retornar os metadados armazenados no DynamoDB.
    #O método é executado com o parâmentro do path Ex.: /images/getMetadata/{s3objectkey}

    file_name = urllib.parse.unquote_plus(event["pathParameters"]["s3objectkey"])

    try:
        response = dynamodb_client.query(
            TableName="serverless-challenge-dev",
            Limit=1,
            ScanIndexForward=False,
            KeyConditionExpression="filename = :key",
            ExpressionAttributeValues={":key" : {"S" : file_name}}
            )
    except Exception as e:
        print ({
            "statusCode": 422,
            "body": json.dumps({"message": "Error '{}' fetching file '{}'".format(e,file_name),}),
            "headers":{}
        })
        raise e
    else:
        #forma a s3objectkey com a coluna folder e a coluna filename do dynamodb
        s3objectkey = response["Items"][0]["folder"]["S"]+"/"+response["Items"][0]["filename"]["S"]
        responseBody = {
            "s3objectkey" : s3objectkey,
            "contentlength" : response["Items"][0]["contentlength"]["N"],
            "contenttype" : response["Items"][0]["contenttype"]["S"],
            "dimension" : response["Items"][0]["dimension"]["S"]
        }
        return {
            "statusCode": 200,
            "body": json.dumps(responseBody)
        }
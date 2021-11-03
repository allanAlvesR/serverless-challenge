# coding=utf-8
import boto3, json
dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client("s3")


def infoImages(event, context):
    #Função InfoImages, que não recebe nenhum parâmetro e pesquisa os metadados salvos no DynamoDB

    try:
        #query da imagem com maior tamanho
        max_img = dynamodb_client.query(
            TableName="serverless-challenge-dev",
            IndexName="serverless-challenge-dev_GSI1",
            Limit=1,
            ScanIndexForward=False,
            KeyConditionExpression="folder = :key",
            ExpressionAttributeValues={":key" : {"S" : "uploads"}}
            )
        #query da imagem com menor tamanho
        min_img = dynamodb_client.query(
            TableName="serverless-challenge-dev",
            IndexName="serverless-challenge-dev_GSI1",
            Limit=1,
            ScanIndexForward=True,
            KeyConditionExpression="folder = :key",
            ExpressionAttributeValues={":key" : {"S" : "uploads"}}
            )
        #query de qtds de imagens
        result_types_qty = dynamodb_client.query(
            TableName="serverless-challenge-dev",
            IndexName="serverless-challenge-dev_GSI2",
            ScanIndexForward=True,
            KeyConditionExpression="folder = :key AND begins_with(contenttype, :type)",
            ExpressionAttributeValues={
            ":key" : {"S" : "uploads"},
            ":type": {"S": "image"}
            })
        types_qty = result_types_qty["Count"]
    except Exception as e:
        print ({
            "statusCode": 422,
            "body": json.dumps({"message": "Error '{}'".format(e),}),
            "headers":{}
        })
        raise e
    else:
        responseBody = {
            "Image com o maior tamanho : " : max_img["Items"][0]["filename"],
            "Image com o menor tamanho : " : min_img["Items"][0]["filename"],
            "Quantidade de de imagens jpg : " : types_qty
        }
        return {
            "statusCode": 200,
            "body": json.dumps(responseBody)
        }
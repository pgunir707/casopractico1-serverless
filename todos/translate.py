import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')

def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    language =  'es'
    
    if "language" in event['pathParameters']:
        language = event['pathParameters']['language']
    
    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    
    client = boto3.client("translate", region_name="us-east-1")
    translated_text = client.translate_text(Text=result['Item']['text'], SourceLanguageCode="auto", TargetLanguageCode=language)
    
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(translated_text)
    }

    return response
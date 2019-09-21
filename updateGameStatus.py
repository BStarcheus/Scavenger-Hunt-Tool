import json
import os
import boto3
from urllib.parse import parse_qs

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):

    table = dynamodb.Table('Scavenger-Hunt-Game')

    params = parse_qs(event['body'])
    status = params['gameStatus'][0]

    item = {
        'gameStatus': status
    }

    # write the todo to the database
    table.put_item(Item=item)

    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }

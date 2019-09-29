import json
import os
import boto3
from urllib.parse import parse_qs

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):

    table = dynamodb.Table('Scavenger-Hunt-Game')

    row = table.get_item(Key={'id': 1})

    if 'gameStatus' not in row['Item']:
        return {
            'statusCode': 400,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': "Error. Could not get status."
        }

    gameStatus = row['Item']['gameStatus']
    return {
        'statusCode': 200,
        'headers': {"Access-Control-Allow-Origin": "*"},
        'body': gameStatus
    }

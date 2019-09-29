import json
import os
import boto3
from urllib.parse import parse_qs

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):

    table = dynamodb.Table('Scavenger-Hunt-Teams')

    params = parse_qs(event['body'])


    if 'teamName' not in params:
        return {
            'statusCode': 400,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': "Error. Team could not be created."
        }

    teamName = params['teamName'][0]
    teamPassword = params['teamPassword'][0]

    item = {
        'teamName': teamName,
        'password': teamPassword
    }

    putReply = table.put_item(Item=item)

    if putReply['ResponseMetadata']['HTTPStatusCode'] == 200:
        bod = "{} created.".format(teamName)
        return {
            'statusCode': 200,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': bod
        }
    else:
        return {
            'statusCode': 400,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': "Error. Team could not be created."
        }

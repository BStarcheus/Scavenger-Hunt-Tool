import json
import os
import boto3
from urllib.parse import parse_qs

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):

    table = dynamodb.Table('Scavenger-Hunt-Teams')

    params = parse_qs(event['body'])


    if 'teamName' not in params:
        logging.error("No team name given.")
        raise Exception("Couldn't create the team.")

    teamName = params['teamName'][0]
    teamPassword = params['teamPassword'][0]

    item = {
        'teamName': teamName,
        'password': teamPassword
    }

    # write the todo to the database
    table.put_item(Item=item)

    return {
        'statusCode': 200,
        'body': json.dumps(params)
    }

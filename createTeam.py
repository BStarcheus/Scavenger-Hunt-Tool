import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):

    table = dynamodb.Table('Scavenger-Hunt-Teams')

    params = event['queryStringParameters']

    teamName = params['teamName']
    teamPassword = params['password']

    item = {
        'teamName': teamName,
        'password': teamPassword
    }

    # write the todo to the database
    table.put_item(Item=item)

    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }

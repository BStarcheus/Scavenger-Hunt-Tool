import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):

    tableGame = dynamodb.Table('Scavenger-Hunt-Game')

    game = tableGame.get_item(Key={'id': 1})

    if 'gameStatus' not in game['Item']:
        return {
            'statusCode': 299,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': "Error. Could not get status."
        }

    gameStatus = game['Item']['gameStatus']
    return {
        'statusCode': 200,
        'headers': {"Access-Control-Allow-Origin": "*"},
        'body': gameStatus
    }

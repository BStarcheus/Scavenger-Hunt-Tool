import json
import os
import boto3
from urllib.parse import parse_qs

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):

    tableTeams = dynamodb.Table('Scavenger-Hunt-Teams')
    tableGame = dynamodb.Table('Scavenger-Hunt-Game')

    #Get the number of tasks in the game.
    game = tableGame.get_item(Key={'id': 1})

    if 'Item' not in game:
        return {
            'statusCode': 299,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': "Error. No game set up."
        }

    numTasks = int(game['Item']['tasks'])
    if numTasks < 1:
        return {
            'statusCode': 280,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': "Error. Game has invalid number of tasks."
        }

    params = parse_qs(event['body'])

    if 'teamName' not in params:
        return {
            'statusCode': 250,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': "Error. No team name given."
        }

    teamName = params['teamName'][0]
    teamPassword = params['teamPassword'][0]

    item = {
        'teamName': teamName,
        'password': teamPassword
    }
    # Start each team off with no tasks complete.
    for i in range(1, numTasks + 1):
        tempTask = 'task{}'.format(i)
        item[tempTask] = 0

    # Add the new team to the database.
    try:
        putReply = tableTeams.put_item(Item=item, ConditionExpression="attribute_not_exists(teamName)")
    except:
        return {
            'statusCode': 297,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': "Error. That team name is already taken."
        }

    if putReply['ResponseMetadata']['HTTPStatusCode'] == 200:
        bod = "{} created.".format(teamName)
        return {
            'statusCode': 200,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': bod
        }
    else:
        return {
            'statusCode': 299,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': "Error. Team could not be created."
        }

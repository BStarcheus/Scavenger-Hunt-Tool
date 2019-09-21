import json
import os
import boto3
from urllib.parse import parse_qs

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):

    tableTasks = dynamodb.Table('Scavenger-Hunt-Tasks')
    tableTeams = dynamodb.Table('Scavenger-Hunt-Teams')

    params = parse_qs(event['body'])
    taskNum = params['taskNum'][0]
    teamName = params['teamName'][0]
    teamPassword = params['teamPassword'][0]
    answer = params['answer'][0]

    taskRow = tableTasks.get_item(
        Key={
            'id': taskNum
        })

    correctAnswer = taskRow['Item']['answer']

    teamRow = tableTeams.get_item(
        Key={
            'teamName': teamName
        })

    correctPassword = teamRow['Item']['password']

    nextLocationHint = taskRow['Item']['nextLocationHint']


    if password == correctPassword:
        if answer == correctAnswer:

            message = "Correct answer." + nextLocationHint
            response = {
                'statusCode': 200,
                'body': message
            }

            update_expr = 'SET task{} = :val1'.format(taskNum)

            teamRow.update_item(
                Key={'teamName': teamName},
                UpdateExpression=update_expr,
                ExpressionAttributeValues={':val1': 1}
            )

        else:
            #Answer incorrect
            response = {
                'statusCode': 300,
                'body': 'Wrong answer. Try again.'
            }
    else:
        #Password incorrect
        response = {
            'statusCode': 400,
            'body': 'Password incorrect.'
        }

    return response

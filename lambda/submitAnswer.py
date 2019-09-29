import json
import os
import boto3
from urllib.parse import parse_qs

dynamodb = boto3.resource('dynamodb')

def isWinner(table, name):
    tableTeams = dynamodb.Table('Scavenger-Hunt-Teams')
    tableGame = dynamodb.Table('Scavenger-Hunt-Game')
    teamRow = table.get_item(
        Key={
            'teamName': name
        })
    row = tableGame.get_item(Key={'id': 1})

    if len(teamRow['Item']) > 0 and row['Item']['gameStatus'] != "Game in progress":
        hasWon = True
        keys = list(teamRow['Item'])
        for col in keys:
            if col[:4] != 'task':
                if teamRow['Item'][col] == 0:
                    hasWon = false
                    break

        if (hasWon):
            tableGame = dynamodb.Table('Scavenger-Hunt-Game')

            val1 = "{} has won the game!".format(name)
            update_expr = 'SET gameStatus = :val1'

            updateReply = tableGame.update_item(
                Key={'id': 1},
                UpdateExpression=update_expr,
                ExpressionAttributeValues={':val1': val1}
            )
            if updateReply['ResponseMetadata']['HTTPStatusCode'] != 200:
                #Error in AWS
                return {
                    'statusCode': 400,
                    'headers': {"Access-Control-Allow-Origin": "*"},
                    'body': "Error. Could not update team table. Try again."
                }


def lambda_handler(event, context):

    tableTasks = dynamodb.Table('Scavenger-Hunt-Tasks')
    tableTeams = dynamodb.Table('Scavenger-Hunt-Teams')

    params = json.loads(event['body'])

    if len(params) < 1:
        response = {
            'statusCode': 450,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': 'Invalid request.'
            }
    else:
        taskNum = params['taskNum']
        teamName = params['teamName']
        teamPassword = params['teamPassword']
        answer = params['answer']

        taskRow = tableTasks.get_item(
            Key={
                'id': int(taskNum)
            })

        correctAnswer = taskRow['Item']['answer']
        nextLocationHint = taskRow['Item']['nextLocationHint']

        teamRow = tableTeams.get_item(
            Key={
                'teamName': teamName
            })

        correctPassword = teamRow['Item']['password']

        if teamPassword == correctPassword:
            if answer == correctAnswer:
                #Change their score for that task from 0 to 1
                update_expr = 'SET task{} = :val1'.format(taskNum)

                updateReply = tableTeams.update_item(
                    Key={'teamName': teamName},
                    UpdateExpression=update_expr,
                    ExpressionAttributeValues={':val1': 1}
                )

                if updateReply['ResponseMetadata']['HTTPStatusCode'] == 200:
                    #Table update was successful
                    message = "Correct answer. Hint to next location: " + nextLocationHint
                    response = {
                        'statusCode': 200,
                        'headers': {"Access-Control-Allow-Origin": "*"},
                        'body': message
                    }
                    isWinResponse = isWinner(tableTeams, teamName)
                    if isWinResponse:
                        return isWinResponse
                else:
                    #Error in AWS
                    response = {
                        'statusCode': 400,
                        'headers': {"Access-Control-Allow-Origin": "*"},
                        'body': "Error. Could not update team table. Try again."
                    }
            else:
                #Answer incorrect
                response = {
                    'statusCode': 300,
                    'headers': {"Access-Control-Allow-Origin": "*"},
                    'body': 'Wrong answer. Try again.'
                }
        else:
            #Password incorrect
            response = {
                'statusCode': 350,
                'headers': {"Access-Control-Allow-Origin": "*"},
                'body': 'Password incorrect.'
            }

    return response

import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')

def updateWinner(tableT, tableG, name, status):
    if status != "Game in progress":
        # Someone has already won.
        # The player can still submit their answer and play the game,
        # they just can't win.
        return

    # Get the updated progress of the team.
    teamRow = tableT.get_item(Key={'teamName': name})

    if len(teamRow['Item']) > 0:
        hasWon = True
        keys = list(teamRow['Item'])
        for col in keys:
            if col[:4] == 'task':
                if teamRow['Item'][col] == 0:
                    hasWon = False
                    break

        if (hasWon):
            val1 = "{} has won the game!".format(name)
            update_expr = 'SET gameStatus = :val1'

            updateReply = tableG.update_item(
                Key={'id': 1},
                UpdateExpression=update_expr,
                ExpressionAttributeValues={':val1': val1}
            )
            if updateReply['ResponseMetadata']['HTTPStatusCode'] != 200:
                #Error in AWS
                return {
                    'statusCode': 290,
                    'headers': {"Access-Control-Allow-Origin": "*"},
                    'body': "Error. Could not update team table. Try again."
                }


def lambda_handler(event, context):

    tableGame = dynamodb.Table('Scavenger-Hunt-Game')
    game = tableGame.get_item(Key={'id': 1})

    if 'Item' not in game:
        return {
            'statusCode': 299,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': "Error. No game set up."
        }

    if game['Item']['gameActive'] != 1:
        # If the game has not started, do not accept any answers
        return {
            'statusCode': 250,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': 'Game has not yet started.'
        }
    gameStatus = game['Item']['gameStatus']

    tableTasks = dynamodb.Table('Scavenger-Hunt-Tasks')
    tableTeams = dynamodb.Table('Scavenger-Hunt-Teams')

    params = json.loads(event['body'])

    if len(params) < 1:
        response = {
            'statusCode': 299,
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

        if 'Item' not in taskRow:
            return {
                'statusCode': 298,
                'headers': {"Access-Control-Allow-Origin": "*"},
                'body': "Invalid task number."
            }

        correctAnswer = taskRow['Item']['answer']
        nextLocationHint = taskRow['Item']['nextLocationHint']

        teamRow = tableTeams.get_item(Key={'teamName': teamName})
        if 'Item' not in teamRow:
            # User does not exist
            return {
                'statusCode': 285,
                'headers': {"Access-Control-Allow-Origin": "*"},
                'body': "Team does not exist."
            }

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

                    isWinResponse = updateWinner(tableTeams, tableGame, teamName, gameStatus)
                    if isWinResponse:
                        return isWinResponse
                else:
                    #Error in AWS
                    response = {
                        'statusCode': 280,
                        'headers': {"Access-Control-Allow-Origin": "*"},
                        'body': "Error. Correct answer but could not update team table. Try again."
                    }
            else:
                #Answer incorrect
                response = {
                    'statusCode': 230,
                    'headers': {"Access-Control-Allow-Origin": "*"},
                    'body': 'Wrong answer. Try again.'
                }
        else:
            #Password incorrect
            response = {
                'statusCode': 220,
                'headers': {"Access-Control-Allow-Origin": "*"},
                'body': 'Password incorrect.'
            }

    return response

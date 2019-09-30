#This file is to be run by the game admin only. Not for AWS deployment.

import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')

tableGame = dynamodb.Table('Scavenger-Hunt-Game')

update_expr = 'SET gameStatus = :val1, gameActive = :val2'

updateReply = tableGame.update_item(
    Key={'id': 1},
    UpdateExpression=update_expr,
    ExpressionAttributeValues={':val1': 'Game in progress', ':val2': 1}
)
if updateReply['ResponseMetadata']['HTTPStatusCode'] == 200:
    #Table update was successful
    print('Game started.')
else:
    print('Game could not be started.')

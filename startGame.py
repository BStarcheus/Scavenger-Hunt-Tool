#This file is to be run by the game admin only. Not for AWS deployment.

import json
import os
import boto3
from urllib.parse import parse_qs

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Scavenger-Hunt-Game')

update_expr = 'SET gameStatus = :val1 gameActive = :val2'
val1 = "Game in progress"

updateReply = tableGame.update_item(
    Key={'id': 1},
    UpdateExpression=update_expr,
    ExpressionAttributeValues={':val1': val1, ':val2': 1}
)
if updateReply['ResponseMetadata']['HTTPStatusCode'] == 200:
    #Table update was successful
    print('Game started.')
else:
    print('Game could not be started.')

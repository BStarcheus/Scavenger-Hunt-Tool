#This file is to be run by the game admin only. Not for AWS deployment.

import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')

tableGame = dynamodb.Table('Scavenger-Hunt-Game')
tableTasks = dynamodb.Table('Scavenger-Hunt-Tasks')

numTasks = int(input("Enter the number of tasks for the game: "))

item = {
    'id': 1,
    'gameActive': 0,
    'gameStatus': 'Stopped',
    'tasks': numTasks
}
# Initialize the Game table
putReply = tableGame.put_item(Item=item)

# Enter the information for each task and insert into the Tasks table
i = 1
while i <= numTasks:
    q = input("Enter the question for task {}: ".format(i))
    a = input("Enter the answer for task {}: ".format(i))
    locHint = input("Enter the next location hint a team should receive after completing task {}: ".format(i))

    item = {
        'id': i,
        'question': q,
        'answer': a,
        'nextLocationHint': locHint
    }
    putReply = tableTasks.put_item(Item=item)

    if putReply['ResponseMetadata']['HTTPStatusCode'] == 200:
        i += 1
    else:
        print("Error inserting item into Tasks table. Try again.")

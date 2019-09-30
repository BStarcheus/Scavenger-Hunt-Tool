# Scavenger-Hunt-Tool
A tool to create a scavenger hunt game and deploy to AWS.


# Configuration

## AWS DynamoDB

Create tables:  
- 'Scavenger-Hunt-Teams'  
- 'Scavenger-Hunt-Game'  
- 'Scavenger-Hunt-Tasks'  

In 'Scavenger-Hunt-Game' insert a row:  
- id: 1  
- gameActive: 0  
- gameStatus: "Stopped"  
- tasks: NUMBER_OF_TASKS_FOR_YOUR_GAME  

In 'Scavenger-Hunt-Tasks' insert a row for each task:  
- id: TASK_NUMBER_STARTING_AT_0  
- question: YOUR_QUESTION  
- answer: YOUR_ANSWER  
- nextLocationHint: YOUR_HINT_TO_NEXT_SCAV_HUNT_LOCATION  

## AWS Lambda

Create Functions:  
- 'submitAnswer'  
- 'getGameStatus'  
- 'createTeam'  

## Frontend

In /frontend/signup.html:  
- Insert your HTTP Trigger URL for createTeam.

In /frontend/submission.html:  
- Insert your HTTP Trigger URL for submitAnswer and getGameStatus, in that order.

Host the frontend on your own GitHub Pages site!

## Game organizer setup

`pip install boto3`

Create ~/.aws/credentials
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

Create ~/.aws/config
```
[default]
region=YOUR_REGION
```

Check your DynamoDB database for your region. Ex: us-east-2


# Start the game

`python startGame.py`

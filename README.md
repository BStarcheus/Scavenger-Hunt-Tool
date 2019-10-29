# Scavenger-Hunt-Tool
A tool to create a scavenger hunt game and deploy to AWS.


# Requirements

- [Serverless Framework](https://serverless.com/framework/docs/getting-started/) with [AWS configured](https://serverless.com/framework/docs/providers/aws/guide/credentials/)

- boto3  
`pip install boto3`

- Create ~/.aws/credentials
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

- Create ~/.aws/config
```
[default]
region=YOUR_REGION
```


# Setup

Deploy the service using the Serverless Framework  
`serverless deploy`  


Run setupGame.py and enter your game information, questions, and answers.  
This will initialize the Game and Task tables in DynamoDB.  
`python3 setupGame.py`  


## Frontend

In /frontend/signup.html:  
- Insert your HTTP Trigger URL for createTeam.

In /frontend/submission.html:  
- Insert your HTTP Trigger URL for submitAnswer and getGameStatus, in that order.

Host the frontend on your own GitHub Pages site!


# Start the game

`python3 startGame.py`

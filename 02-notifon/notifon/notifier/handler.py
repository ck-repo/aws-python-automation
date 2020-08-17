import json
import boto3
import os


def notifier(event, context):
    client = boto3.client('sns')
    sns = os.environ['SNSTopic']
    response = client.publish(
        TopicArn=sns,
        Message=json.dumps({'default': json.dumps(event)}),
        MessageStructure='json'
    )

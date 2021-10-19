import json
import logging

from requests.models import Response
import boto3
from typing import Union
import os
import uuid
import requests
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

EMAIL_SENDER = os.environ["EMAIL_SENDER"]
REGION = os.environ["REGION"]
EMAIL_TABLE = os.environ["EMAIL_TABLE"]
MAILGUN_URL = os.environ["MAILGUN_URL"]
MAILGUN_API_KEY = os.environ["MAILGUN_API_KEY"]


def handler(event: dict, context: dict) -> Response:
    body: dict = _get_body_from_event(event)

    try:
        response = _send_ses_email(body)
    except ClientError as e:
        logger.info(e.response['Error']['Message'])
        logger.info("AWS SES error, use Mailgun backup.")
        _send_mailgun_email(body)

    else:
        logger.info("Email sent! Message ID:"),
        logger.info(response['MessageId'])

    _write_to_dynamo(body)

    response = _create_response(body)

    return response


def _get_body_from_event(event: dict):
    body: dict = event["body"]
    body: dict = json.loads(body)
    logging.info(body)
    return body


def _send_ses_email(body: dict):
    SENDER: str = EMAIL_SENDER
    RECIPIENT: str = body["mailAddress"]
    AWS_REGION: str = REGION
    SUBJECT: str = body["subject"]
    CHARSET: str = "UTF-8"
    BODY_TEXT: str = ("Amazon SES Test (Python)"
                      )

    BODY_HTML: str = f"""<html>
    <head></head>
    <body>
    <h1>Amazon SES for failsafe test</h1>
    <p>This email was sent with AWS SES</a>.</p>
    <p> Email content {body["content"]}
    </body>
    </html>
                """

    client: boto3 = boto3.client('ses', region_name=AWS_REGION)

    client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
    )


def _send_mailgun_email(body: dict) -> Union[]:
    subject: str = body["subject"]
    content: str = body["content"]
    mail_address: str = body["mailAddress"]
    mailgun_status: Response = requests.post(
        MAILGUN_URL,
        auth=("api", MAILGUN_API_KEY),
        data={"from": f'"INFO" mailgun@{EMAIL_SENDER}',
              "to": [mail_address],
              "subject": subject,
              "text": content})

    logger.info(mailgun_status.status_code)
    logger.info(mailgun_status.text)


def _write_to_dynamo(write_object):
    """
        Save email data to a DynamoDb table for safekeeping.
    """
    client = boto3.resource('dynamodb')
    table = client.Table(EMAIL_TABLE)
    write_object["emailId"] = str(uuid.uuid4())
    table.put_item(Item=write_object)


def _create_response(body):
    if "email_status" in body:
        return {
            "status": 400,
            "content": json.dumps(body)
        }
    else:
        return {
            "status": 200,
            "content": json.dumps(body)
        }

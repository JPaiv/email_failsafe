import json
import logging
import boto3
import os
import uuid
import requests
from botocore.exceptions import ClientError


logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

EMAIL_SENDER = os.environ["EMAIL_SENDER"]
REGION = os.environ["REGION"]
MAILGUN_API_KEY = os.environ["MAILGUN_API_KEY"]
EMAIL_TABLE = os.environ["EMAIL_TABLE"]
MAILGUN_URL = os.environ["MAILGUN_BASE_URL"]


def handler(event, context):
    body = _get_body_from_event(event)

    email_status = _send_ses_email(body)

    if not _check_email_status(email_status):
        #If AWS SES has failed use Mailgun as a backup email sender.
        backup_email_status = _send_mailgun_email(body)

    _write_to_dynamo(body)

    response = _create_response(body)

    return response


def _get_body_from_event(event):
    body = event["body"]
    body = json.loads(body)
    logging.info(body)
    return body


def _send_ses_email(body):
    SENDER = EMAIL_SENDER

    RECIPIENT = body["mailAddress"]

    AWS_REGION = REGION

    SUBJECT = body["subject"]

    BODY_TEXT = ("Amazon SES Test (Python)"
                )

    BODY_HTML = f"""<html>
    <head></head>
    <body>
    <h1>Amazon SES for failsafe test</h1>
    <p>This email was sent with AWS SES</a>.</p>
    <p> Email content {body["content"]}
    </body>
    </html>
                """            

    CHARSET = "UTF-8"

    client = boto3.client('ses',region_name=AWS_REGION)

    try:
        response = client.send_email(
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
    except ClientError as e:
        logger.info(e.response['Error']['Message'])

        return False

    else:
        logger.info("Email sent! Message ID:"),
        logger.info(response['MessageId'])

        return True
        
def _check_email_status(email_status):
    if email_status:
        return True
    return False


def _send_mailgun_email(body):
    subject = body["subject"]
    content = body["content"]
    mail_address = body["mailAddress"]
    mailgun_status = requests.post(
            MAILGUN_URL,
            auth=("api", MAILGUN_API_KEY),
            data={"from": f'"INFO" mailgun@{EMAIL_SENDER}',
                "to": [mail_address],
                "subject": subject,
                "text": content})

    logger.info(mailgun_status.status_code)

    logger.info(mailgun_status.text)

    if mailgun_status.status_code != 200:
        return False

    return True


def _write_to_dynamo(write_object):
    """
        Save email data to a DynamoDb table.
    """
    client = boto3.resource('dynamodb')
    table = client.Table(EMAIL_TABLE)
    write_object["emailId"] =  str(uuid.uuid4())
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

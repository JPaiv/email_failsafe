# email_failsafe

Software works in AWS with Lambda backend so no external frameworks were used. 

# How to run:

Paste this command into the terminal: 

curl --header "Content-Type: application/json" 
/ --request POST 
/ --data '{"mailAddress": "<email_address>", "content": <YOUR_CONTENT>, "subject": <YOUR_SUBJECT>}' 
/ https://r6zhv86tb6.execute-api.eu-central-1.amazonaws.com/emails/post

Currently the email address is locked to one specific verified email address. Contact email owner to see if the email sending was succesful.

# Architecture

Client -> API Gateway -> Lambda -> SES /If failure use Mailgun as backup -> DynamoDB 

1. Client sends the data to API Gateway which triggers a AWS Lambda
2. Lambda parses the data and sends the content with SES as an email.
3. If failure the Lambda uses Mailgun as a backup.
4. Save the data to DynamoDB.

# Future

Have a lambda to check Dynamo table in case both SES and Mailgun failed.

Otherwise this solution can scale up to global requirements. 

# Requirements

1. Docker
2. npm install -g serverless
3. sls plugin install -n serverless-python-requirements or npm install --save serverless-python-requirements
4. Python 3.8 and requests

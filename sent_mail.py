import boto3
import os
customer="shivendra"
id='1234'
HTML_EMAIL_CONTENT = f"""
        <html>
            <head></head>
            <body>
            <h1 style='text-align:center'>This is the heading with {id}</h1>
            <p>Hello, {customer}</p>
            </body>
        </html>
    """




def send_plain_email():
    ses_client = boto3.client("ses", region_name=os.environ.get('REGION_NAME'))
    CHARSET = "UTF-8"
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "shivendra.kaurav@mobigesture.com",
                "rohit.singh@mobigesture.com",
                "satya.goli@mobigesture.com"
                
            ],
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": CHARSET,
                    "Data": f"sample text message {HTML_EMAIL_CONTENT}",
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Amazing Email Tutorial",
            },
        },
        Source="shivudu.deshi@mobigesture.com"
    )
    return response

x=send_plain_email()
print(x)
import boto3
from flask import jsonify
from models_dir.tenant_model import TenantModel
from constants import SNSCodes
from utils.loggingConfig import *

def create_sns_topic(tenant_id, email_list):
    '''
    This function creates an SNS topic based on Organization name which will send subscription requests to whitelisted email addresses in notification configuration
    Parameters:
        tenant_id (int): ID of the tenant
        email_list: list of emails which need to be subscribed to the AWS SNS topic
      
    Return:
        Success: "Success", 200
        Failure: Condition, 400
    '''
    ocr_logger.info("Create SNS function triggered")

    tenant_row = TenantModel.query.filter(TenantModel.Id == tenant_id).first()
    if tenant_row is None:
        ocr_logger.error(SNSCodes.INVALID_TENANT_ID["Error"]["message"])
        return {"Error":SNSCodes.INVALID_TENANT_ID["Error"]},SNSCodes.INVALID_TENANT_ID["status_code"]
    # Create an SNS client
    sns_client = boto3.client('sns')

    # Create the SNS topic and strip all white spaces for AWS SNS name not to have errors
    topic_name = "OCRFailureNotification_" + tenant_row.OrganizationName.replace(" ", "")
    response = sns_client.create_topic(Name=topic_name)

    # Get the TopicArn from the response
    topic_arn = response['TopicArn']
    
    # Subscribe the email addresses to the SNS topic
    for email_address in email_list:
        response = sns_client.subscribe(TopicArn=topic_arn, Protocol="email", Endpoint= email_address)
    
    ocr_logger.info("Create SNS function was successful for tenant: " +str(tenant_id))
    return topic_arn
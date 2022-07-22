import json
from dynamodb import Dynamodb
from boto3.dynamodb.types import TypeDeserializer
import boto3

def lambda_handler(event, context):
    
    # try:
        application_no=event['arguments']['application_no']
        
        #Retriving data from repective table from the event and using application_no as a partition key
        if  event['info']['fieldName']=='listDeliverables':
            tablename='Deliverables'
        elif event['info']['fieldName']=='listRaiseConcern':
            tablename='RaiseConcern'
        else:
            tablename='ChatBox'
        a=Dynamodb()
        dict={'application_no':application_no}
        res=a.querywithsorting(tablename,dict)
    
        return {"items":res}
        
    # except Exception as e :
    #   raise e 
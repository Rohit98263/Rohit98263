import json
from dynamodbclass import Dynamodb
from datetime import timezone
import datetime

def lambda_handler(event, context):
    try:
        #data storing in dynmaodb
        data=event['arguments']['input']
        data['date']=datetime.datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        
        #putting data in repective table using application no(partition key) and date(sort key) and extracting tablename from event '
        if  event['info']['fieldName']=='createDeliverable':
            tablename='Deliverables'
        elif event['info']['fieldName']=='createRaiseConcern':
            tablename='RaiseConcern'
        else:
            tablename='ChatBox'
        a=Dynamodb()
        res=a.putitem(tablename,data)
        
        return data
    except Exception as e:
        raise e
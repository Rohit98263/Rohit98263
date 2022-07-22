import json
from user import User # using getUser layer version 6
from dynamodb import Dynamodb
from datetime import datetime

def lambda_handler(event, context):
    try:
        
        application_no=event['arguments']['input']['application_no']
        status_code=event['arguments']['input']['status_code']
        
        #customer id may or may not be present
        try: 
            customer_id=event['arguments']['input']['customer_id']
        except Exception as e:
            pass
        
        #getting user name from cognito userpool with access token from event
        a=User() 
        cognito_details = a.getUser(event)
        upd_by=cognito_details['name']
        
        #getting status name from 'Status' table with the status code from event
        # here the search is done with get item method because we are searching with primary key data
        tablename='Status'
        searchdict={'status_code':status_code}
        b = Dynamodb()
        res=b.getitems(tablename,searchdict)
        if res.get('Item') is not None:
            formStatus=res['Item']['name']
        else:
            raise Exception("invalid status code")
        
        
        #checking 'SURVEYFORM' table for application no, if exists then updating data otherwise throwing exception
        #Here we are searching with scan beacuse search data is not primary key
        tablename,fieldname,data='SURVEYFORM','application_no',application_no
        res=b.scandynamodb(tablename,fieldname,data)
        
        if len(res['Items'])==0:
            raise Exception(f"record with application no : {application_no} does not exist")
        else: 
            surveyform_id=res['Items'][0]['id']
        
        #inserting status,upd_by,upd_on on SURVEYFORM table with the help of surveyform id from previous reponse 
        updatedata={'upd_by':upd_by,'upd_on':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'formStatus':formStatus
        }
        primary_key_values={'id': surveyform_id}
        res=b.updateitem(tablename,primary_key_values,updatedata)
        return {'message':"success","is_error":False}
    except Exception as e:
        return {'message':f"failed : {e}","is_error":True}
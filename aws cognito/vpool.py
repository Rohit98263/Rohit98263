import boto3
import os
import json

class VLpool:
    def __init__(self,event=None):
        if event is None or type(event)!=dict or len(event) ==0:
            raise Exception(f"event is null or not dict or empty")
            
        if None in (os.environ.get('REGION_NAME'),os.environ.get('POOLID')):
            raise Exception(f"some environment variables are none")
            
        self.client=boto3.client('cognito-idp',region_name=os.environ.get('REGION_NAME'))
        self.poolid = os.environ.get('POOLID')
        self.event = event
        self.dict_list = []
        
    def list_user(self):
        if self.event['users'] == 'all':
            res = self.client.list_users(
            UserPoolId=self.poolid,
            Limit=60)
            
            for details in res['Users']:
                dict ={}
                if details.get('Username') is not None:
                    dict['Username'] = details['Username']
                    for attr in details['Attributes']:
                        dict[attr['Name']] = attr['Value']
                    self.dict_list.append(dict)
                    
        return self.dict_list
        
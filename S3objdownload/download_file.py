import os
import boto3
import json
from dotenv import load_dotenv
from datetime import date, timedelta
# import re
load_dotenv()

# code to get the yesterdays date

class GetFile:
    def __init__(self):
        self.client = boto3.client('s3',region_name = os.environ.get('REGION_NAME'))
        self.resource=boto3.resource('s3',region_name= os.environ.get('REGION_NAME'))
        # self.list_download_items=[]
    def s3object_download(self,bucket_name):
        list_object=self.client.list_objects(Bucket=bucket_name)['Contents']
        print(list_object)
        yesterday = (date.today() - timedelta(days=0)).strftime('20%y-%m-%d')
        if len(list_object)>0:
            cwd=os.getcwd()+"/downloads/"
            files_to_downloaded = []
            for key in list_object:
                file_name=key['Key']
                last_modified=str((key['LastModified']).strftime("%Y-%m-%d" ))
                last_modified=last_modified.split()
                
                if last_modified[0]==yesterday:
                    files_to_downloaded.append(file_name)


                    if file_name in files_to_downloaded:
                        self.client.download_file(bucket_name,key['Key'],cwd+file_name)
               
           
                
        
        

a=GetFile()
bucket_name=os.environ.get('BUCKET_NAME')
test=a.s3object_download(bucket_name)
import boto3
import os

from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.types import TypeDeserializer


class Dynamodb:
    def __init__(self):
        self.client = boto3.client('dynamodb',region_name = os.environ.get('REGION_NAME'))
        self.dynamodb=boto3.resource('dynamodb',region_name= os.environ.get('REGION_NAME'))
        self.Item = {}
        self.attribute = []
        self.keyschema = []
        self.variant = []

    def create(self, tablename, pkey,skey=None):
        """takes table name,partition key or skey if availabe,creats table in dynamodb and returns None
        py:function::
    
        Args:
            tablename(str),pkey(str),skey(str-if available): credentials to be used to create table
        Returns:
            None
        """
        tables =self.getTables()
        try:
            if tablename in tables:
                raise Exception(f"Table name as : {tablename} exists already")

            attributes ={pkey:'HASH'}
            for att in attributes:
                self.attribute.append({
                        'AttributeName': att,
                        'AttributeType': 'S'
                    })
                self.keyschema.append({
                        'AttributeName': att,
                        'KeyType': attributes[att]
                    })
            

            self.table = self.client.create_table(
                AttributeDefinitions= self.attribute,
                TableName=tablename,
                KeySchema= self.keyschema,
                BillingMode='PROVISIONED',
                ProvisionedThroughput={
                    'ReadCapacityUnits': 123,
                    'WriteCapacityUnits': 123
                }
            )
        except Exception as e:
            print(str(e))


    def putitem(self,tablename,dict):
        serializer = boto3.dynamodb.types.TypeSerializer()
        self.Item = {k: serializer.serialize(v) for k,v in dict.items()}
                
        items = self.client.put_item(
            TableName=tablename,
            Item=self.Item
        )
        return items

    def getTables(self):
        """takes none,returns all tables present in dynamodb at a particular region
        py:function::
        Args:
            None
        Returns:
            self.client.list_tables()["TableNames"][list] : list containing tablenames
        
        """
        return self.client.list_tables()["TableNames"]

    def scandynamodb(self,tablename,fieldname,data):
        self.item_table = self.dynamodb.Table(tablename)
        res=self.item_table.scan(
            FilterExpression=Attr(fieldname).eq(data)
        )
        return self.scan_with_LastEvaluatedKey(res,fieldname,data)
       
    def scan_with_LastEvaluatedKey(self,res,fieldname,data):
        """takes response,checks whether LastEvaluatedKey exists or not,if exists performs scan operation in while loop until LastEvaluatedKey exits
        or we get the details for a particular record, returns response 
        """
        while 'LastEvaluatedKey' in res:
            if  res['Count']!=0:
                return res
            LastEvaluatedKey=res['LastEvaluatedKey']
            res= self.item_table.scan( FilterExpression=Attr(fieldname).eq(data) 
            ,ExclusiveStartKey=LastEvaluatedKey)
            
        return res

    def getitems(self,tablename,key):
        """takes table name,primary key details and search items for those records only
        py:function
        
        Args:
            tablename(str):table to be scanned,key(dict): primary key constraints in the table
            
        Returns:
            res(dict)
        """
        self.item_table = self.dynamodb.Table(tablename)
        res=self.item_table.get_item(
        Key=key
        ) 
        return res
        
    def updateitem(self,tablename,primary_key_values,updatedata):
        """takes tablenanme,primary_key_values and updatedata and update values in the corrosponding primary key details
        py:function::
        
        Args:
            tablename(str),primary_key_values(dict):primsry key constraints in the table,updatedata(dict): data to be updated
        
        Returns:
            res(dict)
        """
        table = self.dynamodb.Table(tablename)
        updateExpression,expressionattributevalues='',{}
        for key in updatedata:
            updateExpression=updateExpression+','+key+' = :'+key+ ' '
            expressionattributevalues[':'+key]=updatedata[key]
      
        res=table.update_item(
        Key=primary_key_values
        ,UpdateExpression='SET '+ updateExpression[1:],
        ExpressionAttributeValues=expressionattributevalues
        )
        return res
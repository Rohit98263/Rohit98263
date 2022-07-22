import boto3


class User:
    def __init__(self):
        pass
    
    def getUser(self,event):
        try:
            if 'request' in event and 'headers' in event['request']:
                accesstoken = event['request']['headers'].get('authorization')
            elif 'header' in event:
                accesstoken = event['header'].get('Authorization')
            elif 'params' in event and 'header' in event['params']:
                accesstoken = event['params']['header'].get('accesstoken')
            else:
                raise Exception('Unauthorized Access')
            if accesstoken is not None:
                client = boto3.client('cognito-idp')
                response = client.get_user(
                    AccessToken=accesstoken
                )
                user_details = {}
                for item in response.get("UserAttributes"):
                    user_details[item["Name"]] = item["Value"]
                return user_details
            else:
                raise Exception('Unauthorized Access')
        except Exception as e:
            raise Exception(e)
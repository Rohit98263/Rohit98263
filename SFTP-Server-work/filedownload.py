import pysftp
import datetime
from datetime import date, timedelta



sftpHost="s-d3a5420cf44c48c6a.server.transfer.us-east-1.amazonaws.com"
sftpPort= 22
username="shivendra"
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None  
private_key='/home/osiuser/test/id_rsa'
# path='/home/osiuser/file/'
# path to download file on local
def unix2human(unixtime, fmt = "%Y-%m-%d"):
    return datetime.datetime.utcfromtimestamp(int(unixtime)).strftime(fmt)

def download_file_from_sftpserver(path):
    with pysftp.Connection(host=sftpHost,port=sftpPort,username=username,private_key=private_key,cnopts=cnopts) as sftp:
        print("connected to sftp server")
        
        print(sftp.pwd)
        print(sftp.listdir_attr())
        files_to_downloaded = []
        
        for file in sftp.listdir_attr():
            yesterday = (date.today() - timedelta(days=1)).strftime('20%y-%m-%d')
          
            if len(sftp.listdir_attr()) > 0:
                a=file.st_mtime
                print(unix2human(a))
                date_value=str(unix2human(a)).split()
                # date_value=date_value.split()
                print(date_value)
                if date_value[0]==yesterday:
                    file=str(file).split()[8]
                    print(f"file is {file}")
                    # files=file[8]
                    files_to_downloaded.append(file)
                    if file in files_to_downloaded:
                        # get file from sftp server to local directoary
                        remote_path,localpath="/"+file,path+file
                        sftp.get(remote_path, localpath)
        print(f"file downloaded succesfully from SFTP server")              
            
                    
                    
                    
                
            
                
            
            
            
            
            # get file from sftp server to local directoary
            
        
path='/home/osiuser/file/'
download_file_from_sftpserver(path)


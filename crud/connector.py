
import mysql.connector
import os


class Mysqlconnectordatabase:
    def __init__(self):
        self.connect = mysql.connector.connect(host = "localhost", username = "root",password = os.environ.get("PASSWORD"),database = "rohit")
        self.mycursor = self.connect.cursor()
        if self.connect.is_connected():
            print("connection is successful")
        else:
            print("connection is falied")
        
# a = Mysqlconnectordatabase()
    def create_table(self):
        query = f"create table {table_name} ({schema})"
        table_name = input("enter the table name")
        schema = input("enter the schema")  
        cur = self.mycursor.execute(query)
        self.connect.commit()

# # c = Mysqlconnectordatabase()

# # c.create_table()

    def insert(self):
        id = int(input(f"enter the id\n"))
        name = (input(f"enter the name\n"))
        salary = (input(f"enter the salary\n"))
        table_name = input("enter the table name")
        s = f"insert into {table_name} values(%s,%s,%s)"
        e = (id,name,salary)
        self.mycursor.execute(s,e)
        
        
        self.connect.commit()
        
# # c = Mysqlconnectordatabase()

# # c.insert()    

    def update(self):
        # list = input("enter the update coomand in format:student id primary key,colume name,column value   ").split(",")
        # list[0] = int(list[0])
        table_name = input("enter the table name")
        column_name = input(f"enter column name")
        column_value = input(f"enter the colume_value")
        id = input(f"enter the id")
        
        
        self.mycursor.execute(f"update {table_name} set {column_name} = '{column_value}'  where id = {id}")
        self.connect.commit()

# # c = Mysqlconnectordatabase()

# c.update()         
    def delete(self):
        table_name = input("enter the table name")
        column_name = input(f"enter the column")
        column_value = input(f"enter the colume value")
        
        
        self.mycursor.execute(f"delete from {table_name} where {column_name} = {column_value}")
        self.connect.commit()
        
                
# # c = Mysqlconnectordatabase()

# # c.delete() 
    
        


            
            
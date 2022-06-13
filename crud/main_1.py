
from connector import Mysqlconnectordatabase

try:
    opeartion_to_perform = input("enter 1 for create\n enter 2 for insert\n enter 3 for update\n enter 4 for delete")
    a = Mysqlconnectordatabase()
                
    if opeartion_to_perform.upper() == "1":
        a.create_table()

    if opeartion_to_perform.upper() == "2":
        a.insert()

    if opeartion_to_perform.upper() == "3":
        a.update()

    if opeartion_to_perform.upper() == "4":
        a.delete()
except Exception as e:
    print(f"error is {e}")
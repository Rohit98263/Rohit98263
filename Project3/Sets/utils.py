import re
import sys



def reading_file(file_name):
    """
    checking valid email address in given file

    py:function::

    args:
        file_name(str): txt file as the parameter

    return:
        dict: dictionary of valid mail as keys

    """
    with open(file_name,"r") as f1:
        valid_email = {}
        count_variable = 0
        for email in f1:
            a = email.lower().strip()
            if check(a):
                if valid_email.get(a) is None:
                    valid_email[a] = 1


    return valid_email



def write_file(file3):
    """
    write file in .txt file

    py:function::

    args:
        files(dict): dictionary as the parameter

    return:
        dictionary in .txt file



    """
    with open(sys.argv[3],"w") as f2:
        d = f2.write(str(file3))
    return d

def check(email):
    """
    taking input in the string form string and checking valid email

    py:function::

    Args:
         num(str) : string(email) is given as parameter

    return:
        True or False : return valid email or not
    """
    regex = r'\b[A-Za-z]+[._-]*[A-Za-z0-9]{1,}@[A-Za-z0-9-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return True
    return False
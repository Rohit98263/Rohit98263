# divisibilty of 2

def is_divisible_by_2(num):
    """
    Taking input in the string form and comparing the last digit of string

     py:function::

     Args:
         num(str) : string is given as parameter

    return:
     Bool: 'true' if last digit divisible by 2
    """

    if num[-1] in ("0", "2", "4", "6", "8"):
        return True
    return False


# divisibilty of 3
def is_divisible_by_3(string):
    """
      Takes string,convert into integer,total its digits until single digit obtained and returns it

    py:function::

    Args:
        string(str) : string is given as parameter

    return:
        string
    """
    if len(string) >= 2:
        total = 0
        for char in string:
            total = total + int(char)
        return is_divisible_by_3(str(total))
    else:
        return string


# divisibilty of 4
def is_divisible_by_4(n):
    """
    takes string as input,compare the last two digit of sting and if condition gets valifated then return true

    py:function::


    args:
        n(str) : string is given as parameter

    return:
        Bool: 'true' if last two digit divisible by 4
    """
    if len(n) >= 2:
        total = 0
        for i in range(26):
            if total == int(n[-2:]):
                return True
            else:
                total = 4 * (i + 1)
        if i == 25:
            return False
    else:
        if n == "4" or n == "8":
            return True
        else:
            return False


def is_divisible_by_5(num):
    """
    taking string as input, comparing the last digit of string

    py:function::

    args:
        num(str) : string given as parameter

    return:
        Bool: 'true' if last digit divisible by 5


    """

    if len(num) >= 1 and num[-1] == "0" or num[-1] == "5":
        return True


def is_divisible_by_6(num):
    """
    taking string as input, comparing the last digit of string

    py:function::

    args:
        num(str) : string given as parameter

    return:
        bool
    """
    if is_divisible_by_2(num) and (is_divisible_by_3(num) == "3" or is_divisible_by_3(num) == "6" or is_divisible_by_3(num) == "9"):
        return True
    return False


# Divisibilty of 7
def is_divisible_by_7(x, y):
    """
    take two string parameter,convert into int, apply x = x - y and convert into string and return it

    py:function::

    args:
        x,y(str,str): two string given as parameter

    return:
        bool:'true' or 'false'


    """
    x = int(x)
    y = int(y)
    while x >= y:
        x = x - y
    x = str(x)
    return x == "0"


# Divisibilty of 8
def is_divisible_by_8(n):
    """
    takes string,compare the last three digit and last two digit of string and if condition gets validated then return true

    py:function::


    args:
        n(str) : string is given as parameter

    return:
        bool:'true' or 'false'


    """
    if len(n) >= 3:
        total = 0
        for i in range(125):
            if i == 125:
                return False
            if total == int(n[-3:]):
                return True
            else:
                total = 8 * (i + 1)
    elif len(n) >= 2:
        total = 0
        for i in range(13):
            if i == 13:
                return False
            if total == int(n[-2:]):
                return True
            else:
                total = 8 * (i + 1)

    else:
        if n == "8":
            return True
        else:
            return False


def is_divisible_by_9(num):
    """
    taking string as input, comparing the last digit of string

    py:function::

    args:
        num(str) : string given as parameter

    return:
        bool:'true' or 'false'


    """
    if is_divisible_by_3(num) == "9":
        return True
    return False


def function():
    a = user_input.split(",")
    for num in a:
        if int(num) < 0:
            raise Exception("Number cannot be less than zero")
        if int(num) == 0:
            raise Exception("Number cannot be equal to zero")


        reqresult = ""
        count = 0

        if is_divisible_by_2(num):
            reqresult = reqresult + "2"
            count = count + 1

        if is_divisible_by_3(num) in ("3", "6", "9"):
            if count == 0:
                reqresult = reqresult + "3"
                count = count + 1
            else:
                reqresult = reqresult + ",3"

        if is_divisible_by_4(num):
            if count == 0:
                reqresult = reqresult + "4"
                count = count + 1
            else:
                reqresult = reqresult + ",4"

        if is_divisible_by_5(num):
            if count == 0:
                reqresult = reqresult + "5"
                count = count + 1
            else:
                reqresult = reqresult + ",5"

        if is_divisible_by_6(num):
            if count == 0:
                reqresult = reqresult + "6"
                count = count + 1
            else:
                reqresult = reqresult + ",6"
        if is_divisible_by_8(num):
            if count == 0:
                reqresult = reqresult + "8"
                count = count + 1
            else:
                reqresult = reqresult + ",8"

        if is_divisible_by_9(num):

            if count == 0:
                reqresult = reqresult + "9"
                count = count + 1
            else:
                reqresult = reqresult + ",9"

        if is_divisible_by_7(num, "7"):
            if count == 0:
                reqresult = reqresult + "7"
                count = count + 1
            else:
                reqresult = reqresult + ",7"

        if count >= 1:
            print(f"{num} : is divisible by {reqresult}")
        else:
            print(f"{num} : is not divisible")

# user_input = input("enter the number:")
if __name__=='__main__':
    try:
        user_input = input("enter the number with (,) separator:")
        if user_input == "":
            raise Exception("No input provided!")
        else:
            function()
    except Exception as e:
        print(e)


# if user_input == "":

#     print("No input provided")
#     quit()

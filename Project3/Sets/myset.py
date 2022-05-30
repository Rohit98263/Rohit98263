
def union(file1,file2):
    """
    finding the union of  given two dictionary

    py:function::

    args:
        file1,file2(dict): dictionary as the parameter

    return:
        union of two dictionary
    """
    count = 0
    count_1 = 0
    final_union = {}
    for x in file1:
        if final_union.get(x) is None:
            final_union[x] = 1
        else:
            final_union[x] = final_union[x] + 1
            count = count + 1
    for x in file2:
        if final_union.get(x) is None:
            final_union[x] = 1
        else:
            final_union[x] = final_union[x] + 1
            count_1 = count_1 + 1
    return final_union



def intersection(file1,file2):
    """
    finding the intersection of  given two dictionary

    py:function::

    args:
        file1,file2(dict): dictionary as the parameter

    return:
        intersection of two dictionary
    """
    final_intersection = {}

    for email in file1:
        if email in file2:
            final_intersection[email] = 1

    return final_intersection



def minus(file1,file2):
    """
    finding the minus of  given two dictionary

    py:function::

    args:
        file1,file2(dict): dictionary as the parameter

    return:
        minus of two dictionary
    """
    final_minus = {}
    for email in file1:
        if email not in file2:
            final_minus[email] = 1
    return final_minus

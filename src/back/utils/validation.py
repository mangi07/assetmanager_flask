##################################
# File: validation.py
##################################

import datetime


def check_category_input(i, categories):
    """
    To be used to check if user's choice (given by id)
    exists in the listing pulled from db.

    return: True if id in categories, else False
    """
    if i is None:
        return True
    return i in [id for (id, name) in categories]


#date_pattern = re.compile("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
def check_date_format(d):
    """
    Return: True if string d follows format: YYYY-MM-DD HH:MM:SS
    """
    if d is None:
        return True
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return False
    return True
    #x = date_pattern.match(d)
    #if x is None:
    #    raise Exception("Date must follow format ####-##-## ##:##:##")
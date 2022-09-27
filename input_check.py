# NAME Hung Nguyen
# EMAIL hunghn4@uci.edu
# STUDENT ID 26441523

# input_check.py
"""
This module consists of functions that detect errors in IP address, socket, username, password, post, bio
"""

def is_valid_ip(ip_address:str):
    """
    Check if IP address is valid
    """
    # if each byte is from 0 to 255
    def isIPv4(s):
        try: 
            return str(int(s)) == s and 0 <= int(s) <= 255
        except:
            return False
        
    # if the IP address has 3 dots    
    try:    
        if (ip_address.count(".") == 3) and (all(isIPv4(i) for i in ip_address.split("."))):
            return True
        else:
            print('ERROR!! Invalid IP address')
            return False
    except:
        print('ERROR!! Invalid IP address')
        return False


def is_valid_port(port:int):
    """
    Check if port value is integer and from 1 to 65535
    """
    if type(port) == int and 1 <= port <= 65535:
        return True
    else:
        print('ERROR!! Invalid port value')
        return False


def is_valid_str(input_str:str, obj:str):
    """
    Check if input string is empty or just whitespace
    Used for post and bio
    """
    try:
        if (input_str.isspace()) or (input_str == ""):
            print('ERROR!! Invalid', obj)
            return False
        else:
            return True
    except:
        print('ERROR!! Invalid', obj)
        return False


def is_valid_usr_pwd(input_str:str, obj:str):
    """
    Check if input string is valid.
    Return False if the input string is empty or has whitepsace or contains a special character
    Used for username and password
    """
    try:
        if (input_str.isspace()) or (input_str == "") or (" " in input_str):
            print('ERROR!! Invalid', obj)
            return False
        
        # List all the special characters
        special_ch = '[@_!#$%^&*()<>?/\|}{~:+-;,.]'
        # If the input string consists at least one of them
        for ch in input_str:
            if ch in special_ch:
                print('ERROR!! Please do not use any special character')
                return False
    except:
        print('ERROR!! Invalid', obj)
        return False

    return True  
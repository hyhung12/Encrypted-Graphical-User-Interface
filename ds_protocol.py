# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME Hung Nguyen
# EMAIL hunghn4@uci.edu
# STUDENT ID 26441523

import socket
import json
from collections import namedtuple
import connection as conn
from Profile import Post, Profile

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('response', ['type','message'])

def extract_json(json_msg:str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert it to a DataTuple object
  
    TODO: replace the pseudo placeholder keys with actual DSP protocol keys
    '''
    try:
        json_obj = json.loads(json_msg)
        msg_type = json_obj['response']['type']
        msg = json_obj['response']['message']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return DataTuple(msg_type, msg)


def connect_to_server(host:str, port:int) -> socket.socket:
    """
    Create a socket object and connect to the server
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock
    except:
        return None

    
def join(conn_obj, usrn:str, pwd:str, my_public_key):
    """
    Get the username and password then initiate a connection with the ICS 32 DS server
    Return the json messsage and token from the server
    """
    # Initialize a dictionary that follows "join" format
    join_dict = {"join": {"username": usrn,"password": pwd, "token": my_public_key}}
    # Convert to string using json.dumps()
    json_join = json.dumps(join_dict)
    # Send the "string dictonary" to the DS server
    conn._write_command(conn_obj, json_join)
    # Get the response
    json_msg = conn._read_command(conn_obj)
    # Get the token if successfully connecting to the server
    # Return token = None if fail to connect to the server
    user_token = None
    try:
        json_obj = json.loads(json_msg)
        msg_type = json_obj['response']['type']
        if msg_type == "ok":
            user_token = json_obj['response']['token']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
    
    return json_msg, user_token


def post(conn_obj, user_token:str, post:str):
    """
    Get the token and journal post then send the post to the ICS 32 DS server
    Return the json messsage 
    """    
    p = Post(post)
    post_dict = {"token": user_token, "post": p}
    json_post = json.dumps(post_dict)
    conn._write_command(conn_obj, json_post)
    json_msg = conn._read_command(conn_obj)
    return json_msg


def bio(conn_obj, user_token:str, bio:str):
    """
    Get the token and bio then send the bio to the ICS 32 DS server
    Return the json messsage 
    """
    bio_dict = {"token": user_token, "bio": {"entry": bio}}
    json_bio = json.dumps(bio_dict)
    conn._write_command(conn_obj, json_bio)
    json_msg = conn._read_command(conn_obj)
    return json_msg


def ok(json_msg:str):
    """
    Get the response from the server and output OK message
    """    
    datatuple = extract_json(json_msg)
    if datatuple.type == 'ok':
        output_msg = datatuple.type.upper() + '!! ' + datatuple.message
        print(output_msg)
        return True
    else:
        return False

        
def error(json_msg:str):
    """
    Get the response from the server and output ERROR message
    """    
    datatuple = extract_json(json_msg)
    if datatuple.type == 'error':
        output_msg = datatuple.type.upper() + '!! ' + datatuple.message
        print(output_msg)
        return True
    else:
        return False
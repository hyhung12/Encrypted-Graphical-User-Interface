# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME Hung Nguyen
# EMAIL hunghn4@uci.edu
# STUDENT ID 26441523

import input_check
import ds_protocol
import connection as conn

def send(server:str, port:int, username:str, password:str, public_key:str):
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    
    # Check if user inputs are valid
    # Return True/False
    server_bool = input_check.is_valid_ip(server)
    port_bool = input_check.is_valid_port(port)
    usn_bool = input_check.is_valid_usr_pwd(username, 'username')
    pwd_bool = input_check.is_valid_usr_pwd(password, 'password')
    
    is_valid_input = all([server_bool, port_bool, usn_bool, pwd_bool])
    # If all inputs are correct then send all to the server
    if is_valid_input:
        # Create a socket object then perform join, post, bio
        # After executing each function, check if the response from the server is ok
        try:
            sock = ds_protocol.connect_to_server(server, port)
            conn_obj = conn.init(sock)
            join_msg, token = ds_protocol.join(conn_obj, username, password, public_key)
            if ds_protocol.ok(join_msg) and (not ds_protocol.error(join_msg)):   
                return token, conn_obj
            else:
                return None, None
        except:
            return None, None
    else:
        return None, None
    
    return None, None
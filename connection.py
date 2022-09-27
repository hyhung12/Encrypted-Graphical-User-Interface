# NAME Hung Nguyen
# EMAIL hunghn4@uci.edu
# STUDENT ID 26441523

# connection.py

import socket
from collections import namedtuple

# These functions are copied from the lab section

class SMPProtocolError(Exception):
    pass

SMPConnection = namedtuple('SMPConnection',['socket','send','recv'])

def init(sock:socket):
    '''
    The init method should be called for every program that uses the SMP Protocol. The calling program should first establish a connection with a socket object, then pass that open socket to init. init will then create file objects to handle input and output.
    '''
    try:
        f_send = sock.makefile('w')
        f_recv = sock.makefile('r')
    except:
        raise SMPProtocolError("Invalid socket connection")

    return SMPConnection(
        socket = sock,
        send = f_send,
        recv = f_recv
    )

def _write_command(smp_conn: SMPConnection, cmd: str):
    '''
    performs the required steps to send a message, including appending a newline sequence and flushing the socket to ensure
    the message is sent immediately.
    '''
    try:
        smp_conn.send.write(cmd + '\n')
        smp_conn.send.flush()
    except:
        raise SMPProtocolError

def _read_command(smp_conn: SMPConnection):
    '''
    performs the required steps to receive a message. Trims the 
    newline sequence before returning
    '''
    cmd = smp_conn.recv.readline()[:-1]
    return cmd
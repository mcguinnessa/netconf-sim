#!/usr/bin/env python
import logging
import socket
import sys
import threading
from _thread import *

import paramiko

SESSION_TIME = 60


from netconf_subsys import NETCONFsubsys
from netconf_node import NETCONFTestNode

logging.basicConfig()
logger = logging.getLogger()

if len(sys.argv) != 2:
    print("Need private host RSA key as argument.")
    sys.exit(1)

host_key = paramiko.RSAKey(filename=sys.argv[1])



class Server(paramiko.ServerInterface):
    channel = None
    def __init__(self):
        self.event = threading.Event()
        print("Init Server")

        self.node = NETCONFTestNode() 
        NETCONFsubsys.register_callback_object(self.node)


    def check_channel_request(self, kind, chanid):
        print("check_channel_request")
        print("    kind="+str(kind))
        print("  chanid="+str(chanid))
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

#    def check_channel_subsystem_request(self, channel, name):
#        print("check_channel_subsystem_request")
#        print("    kind="+str(channel,))
#        print("  name="+str(name))
#        if name == 'netconf':
#            #return paramiko.OPEN_SUCCEEDED
#            print("Subsystem OK")
#            return True


    def check_auth_publickey(self, username, key):
        print("check_auth_publickey")
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        print("get_allowed_auths")
        return 'publickey'

    def check_channel_exec_request(self, channel, command):
        print("check_channel_exec_request")
        # This is the command we need to parse
        print("Command:" + command)
        print("Channel:" + channel)
        self.event.set()
        return True

def threaded(client):
    t = paramiko.Transport(client)
    t.set_gss_host(socket.getfqdn(""))
    t.load_server_moduli()
    t.add_server_key(host_key)

    server = Server()
    t.set_subsystem_handler('netconf', NETCONFsubsys, server.channel, "netconf", server)

    t.start_server(server=server)
    print("Connected:" + str(server))

    # Wait 30 seconds for a command
    server.event.wait(SESSION_TIME)
    t.close()


   


def listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock.bind(('127.0.0.1', 2222))
    sock.bind(('', 2222))
    print("Bound to 2222")

    sock.listen(100)
    client, addr = sock.accept()

    start_new_thread(threaded, (client,))

#    t = paramiko.Transport(client)
#    t.set_gss_host(socket.getfqdn(""))
#    t.load_server_moduli()
#    t.add_server_key(host_key)
#
#    server = Server()
#    t.set_subsystem_handler('netconf', NETCONFsubsys, server.channel, "netconf", server)
#
#    t.start_server(server=server)
#    print("Connected:" + str(server))
#
#    # Wait 30 seconds for a command
#    server.event.wait(60)
#    t.close()


while True:
    try:
        listener()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as exc:
        logger.error(exc)

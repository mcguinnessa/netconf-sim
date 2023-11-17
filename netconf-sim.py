#!/usr/bin/env python

import logging
import socket
import getopt
import sys
import threading
from _thread import *

from binascii import hexlify
import base64
from paramiko.util import b, u

import paramiko

SESSION_TIME = 60

DEFAULT_PORT = 1830

#port = DEFAULT_PORT

from netconf_subsys import NETCONFsubsys
from netconf_node import NETCONFTestNode

def usage():
   print("Needs at least one argument for RSA private key")
   sys.exit(1)


class NetconfServer(paramiko.ServerInterface):
    channel = None
    def __init__(self, user):
        self.event = threading.Event()
        logging.debug("Init Server")

        self.node = NETCONFTestNode() 
        NETCONFsubsys.register_callback_object(self.node)
        self.user = user


    def check_channel_request(self, kind, chanid):
        logging.debug("check_channel_request")
        logging.debug("    kind="+str(kind))
        logging.debug("  chanid="+str(chanid))
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
        logging.debug("check_auth_publickey")
        logging.debug("username:" + str(username))
#        logging.debug("key:" + str(key))
          
#        return paramiko.AUTH_SUCCESSFUL
#        print("Auth attempt with key: " + str(hexlify(key.get_fingerprint())))
        logging.debug("Auth attempt with key: " + u(hexlify(key.get_fingerprint())))
#        if (username == "robey") and (key == self.good_pub_key):
        if (username == self.user) :
            return paramiko.AUTH_SUCCESSFUL
#        return paramiko.AUTH_FAILED


    def get_allowed_auths(self, username):
        logging.debug("get_allowed_auths")
        return 'publickey'

    def check_channel_exec_request(self, channel, command):
        logging.debug("check_channel_exec_request")
        # This is the command we need to parse
        logging.debug("Command:" + command)
        logging.debug("Channel:" + channel)
        self.event.set()
        return True

def threaded(client, key_file, user):

    logging.debug("Thread")
    t = paramiko.Transport(client)
    t.set_gss_host(socket.getfqdn(""))
    t.load_server_moduli()

    logging.debug("Private Key file:" + str(key_file))

    host_key = paramiko.RSAKey(filename=key_file)

    logging.debug("Read key: " + u(hexlify(host_key.get_fingerprint())))
    t.add_server_key(host_key)

    server = NetconfServer(user)
    t.set_subsystem_handler('netconf', NETCONFsubsys, server.channel, "netconf", server)

    t.start_server(server=server)
    logging.info("Connected:" + str(server))

    # Wait 30 seconds for a command
    server.event.wait(SESSION_TIME)
    t.close()


   


def listener(port, private_key_file, user):

    #port = g_port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock.bind(('127.0.0.1', 2222))
    sock.bind(('', port))
    logging.info("Listening to " + str(port))

    sock.listen(100)
    client, addr = sock.accept()

    start_new_thread(threaded, (client, private_key_file, user))

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




#########################################################################################
#
# Main
#
#########################################################################################
def main(argv):

   port = DEFAULT_PORT
   user = ""

   try:
      opts, args = getopt.getopt(argv, "p:k:l:u:", ["log=", "port=", "rsa-key=", "user="])
   except getopt.GetoptError:
      usage()
      sys.exit(2)

   
   loglevel = "INFO"
   for opt, arg in opts:
      if opt in ("-l", "--log"):
         loglevel = arg.upper()
         print("loglevel:" + str(loglevel))
      if opt in ("-u", "--user"):
         user = str(arg)
         print("user:" + str(user))
      if opt in ("-k", "--rsa-key"):
         private_key_file = arg
         print("Private Key file:" + str(private_key_file))
      if opt in ("-p", "--port"):
         port = int(arg)
         print("Port " + str(port) + " provided")


   numeric_log_level = getattr(logging, loglevel, None)

   #logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='./netconf-sim.log', filemode='w', level=logging.DEBUG)
   #logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='netconf-sim.log', filemode='w')
   formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')

   #formatter = logging.Formatter('%(message)s')
   logging.getLogger('').setLevel(loglevel)
   fh = logging.FileHandler('./netconf-sim.log', mode='w')
   fh.setLevel(loglevel)
   fh.setFormatter(formatter)
   logging.getLogger('').addHandler(fh)

   ch = logging.StreamHandler()
   ch.setLevel(loglevel)
   ch.setFormatter(formatter)  
   logging.getLogger('').addHandler(ch)

   logging.info("NETCONF Simulator")

   #host_key = paramiko.RSAKey(filename=sys.argv[1])


   while True:
       try:
           listener(port, private_key_file, user)
       except KeyboardInterrupt:
           sys.exit(0)
       except Exception as exc:
           logging.error(exc)


if __name__ == "__main__":
   main(sys.argv[1:])


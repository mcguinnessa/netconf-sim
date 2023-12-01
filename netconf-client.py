#!/usr/bin/env python


from ncclient import manager

import sys
import getopt
import logging
import time



#host = "barnes.home.lan"
#host = "www.rocket-surgery.co.uk"
#port = 830
#port = 1830
#username = "alex"

#########################################################################################
#
# Main
#
#########################################################################################
def main(argv):

   try:
      opts, args = getopt.getopt(argv, "h:p:u:l:t:", ["port=", "host=", "user=", "log=", "timeout="])
   except getopt.GetoptError:
      usage()
      sys.exit(2)

   host = None
   port = None
   user = None
   timeout = 30

   loglevel = "INFO"

   for opt, arg in opts:
      if opt in ("-l", "--log"):
         loglevel = arg.upper()
         print("Log:" + str(loglevel))
      if opt in ("-h", "--host"):
         host = str(arg)
         print("Host:" + host)
      if opt in ("-u", "--user"):
         user = arg
         print("user:" + str(user))
      if opt in ("-p", "--port"):
         port = int(arg)
         print("Port " + str(port) + " provided")
      if opt in ("-t", "--timeout"):
         timeout = int(arg)
         print("Timeout " + str(timeout) )

   if host is None or port is None or user is None:
      print("Needs arguments for port, host and user")
      usage()
      sys.exit(1) 


   numeric_log_level = getattr(logging, loglevel, None)

   #logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='./netconf-sim.log', filemode='w', level=logging.DEBUG)
   #logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='netconf-sim.log', filemode='w')
   logging.getLogger("ncclient").setLevel(loglevel)
   formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')

   #formatter = logging.Formatter('%(message)s')
   #logging.getLogger('').setLevel(logging.DEBUG)
   logging.getLogger('').setLevel(loglevel)
   fh = logging.FileHandler('./netconf-client.log', mode='w')
   fh.setLevel(loglevel)
   fh.setFormatter(formatter)
   logging.getLogger('').addHandler(fh)

   ch = logging.StreamHandler()
   ch.setLevel(loglevel)
   ch.setFormatter(formatter)
   logging.getLogger('').addHandler(ch)

   logging.info("NETCONF Client")


   eos=manager.connect(host=host, port=port, timeout=timeout, username=user, password="", hostkey_verify=False, key_filename='/home/alex/.ssh/id_rsa')
   logging.info("Connected: " + str(eos.connected))

   for cap in eos.server_capabilities:
      logging.info("Capability:" + str(cap))



   logging.debug("Sending get-config")
   resp = eos.get_config(source="running")
   logging.info("resp:" + str(resp))

   delay = 1
   logging.info("Sleeping for "+str(delay)+"s")
   time.sleep(delay)


   conf = """
      <config>
         <system xmlns="http://openconfig.net/yang/system">
            <config>
               <domain-name>abc.xyz</domain-name>
            </config>
         </system>
      </config>"""

   logging.debug("Sending edit-config")
   eos.edit_config(target = "running", config = conf, default_operation="merge")

   logging.info("Sleeping for "+str(delay)+"s")
   time.sleep(delay)

#<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:33ca18d3-43b5-4277-a6ce-9a751f74cada"><ok></ok></rpc-reply>

   logging.debug("Sending close-session")
   resp = eos.close_session()

   #eos.connected
   #eos.timeout 30
   #eos.session_id  '1292406600'

def usage():
   print("netconf-client -p <port> -h <host> -u <user> -t <timeout> -l <loglevel>")


if __name__ == "__main__":
   main(sys.argv[1:])



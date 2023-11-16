#!/usr/bin/env python


from ncclient import manager

import sys
import getopt



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
      opts, args = getopt.getopt(argv, "h:p:u:", ["port=", "host=", "user="])
   except getopt.GetoptError:
      usage()
      sys.exit(2)

   host = None
   port = None
   user = None

   for opt, arg in opts:
      if opt in ("-h", "--host"):
         host = str(arg)
         print("Host:" + host)
      if opt in ("-u", "--user"):
         user = arg
         print("user:" + str(user))
      if opt in ("-p", "--port"):
         port = int(arg)
         print("Port " + str(port) + " provided")

   if host is None or port is None or user is None:
      print("Needs arguments for port, host and user")
      sys.exit(1) 


   eos=manager.connect(host=host, port=port, timeout=30, username=user, password="", hostkey_verify=False)
   print("Connected: " + str(eos.connected))

   for cap in eos.server_capabilities:
      print("Capability:" + str(cap))



   print("Sending get-config")
   resp = eos.get_config(source="running")
   print("resp:" + str(resp))

   #eos.connected
   #eos.timeout 30
   #eos.session_id  '1292406600'


if __name__ == "__main__":
   main(sys.argv[1:])



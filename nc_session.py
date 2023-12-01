
import xml.etree.ElementTree as ET
import logging

from netconf_spec import *
from nc_socket import NCSocket


#READ_SIZE = 1024


class NCSession():

   def __init__(self, sock):
      logging.debug("NCSocket init")
      self.sock = NCSocket(sock)
      self.version = NC_BASE_1_0


###################################################################################
#
# Gets the NETCONF message
#
###################################################################################
   def read_message(self):
      self.version, request = self.sock.read_message()
      return request

###################################################################################
#
# Writes the NETCONF base 1.0 message 
#
###################################################################################
   def write_message(self, message):

      if self.version == NC_BASE_1_1:
         self.sock.write_message_1_1(message)
      else:
         self.sock.write_message_1_0(message)

###################################################################################
#
# Close
#
###################################################################################
   def close(self):
      #self.sock.flush() 
      self.sock.close()

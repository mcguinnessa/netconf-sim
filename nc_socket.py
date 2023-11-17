
import xml.etree.ElementTree as ET
import logging

from netconf_subsys import NC_TERMINATOR


READ_SIZE = 1024


class NCSocket():

   def __init__(self, sock):
      logging.debug("NCSocket init")
      self.sock = sock
      self.buffer = b''
      self.term_as_bytes = str.encode(NC_TERMINATOR)


###################################################################################
#
# Gets the NETCONF message
#
###################################################################################
   def read_message(self):
      logging.debug("NETCONFTestNode handle_session")

      self.buffer = b''
      while self.term_as_bytes not in self.buffer:
         if self.sock.recv_ready():
            data = self.sock.recv(READ_SIZE)
            if not data:
               """Not read anything"""

            self.buffer += data
            logging.debug("buffer:" + str(self.buffer))

      logging.debug("FINAL: buffer:" + str(self.buffer))

      request = self.buffer.decode()
      logging.debug("RAW: request:" + str(request))
      request = request.split(']]>]]>', 1)[0]
      request = request.strip()



      #request = request.replace(']]>]]>', '')
      logging.debug("FINAL: request:" + request)
#      print("FINAL: request type:" + str(type(request)))
      return request

###################################################################################
#
# Close
#
###################################################################################
   def close(self):
      #self.sock.flush() 
      self.sock.close()

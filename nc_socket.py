
import xml.etree.ElementTree as ET
import logging
import re

#from netconf_spec import NC_TERMINATOR_1_0
from netconf_spec import *


READ_SIZE = 1024


class NCSocket():

   def __init__(self, sock):
      logging.debug("NCSocket init")
      self.sock = sock
      self.buffer = b''
      self.term_as_bytes = str.encode(NC_TERMINATOR_1_0)
      self.terminators = [str.encode(NC_TERMINATOR_1_0), str.encode(NC_TERMINATOR_1_1)]

      self.pattern_10 = re.compile('(.*)]]>]]>' )
      #self.pattern_11 = re.compile('\n#(\d+)\n(.*)\n##\n')
      self.pattern_11 = re.compile('\n#(\d+)\n(.*)\n##\n', re.DOTALL) #DOTALL allows '.' to match all including newlines

      #self.pattern_11 = re.compile("""\n#(480)\n(.*)""", re.DOTALL)

#\n#480\n<?xml version="1.0" encoding="UTF-8"?><nc:rpc xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:236852ab-50ce-4989-ab34-49f86511a918"><nc:edit-config><nc:target><nc:running/></nc:target><nc:default-operation>merge</nc:default-operation><config>\n         <system xmlns="http://openconfig.net/yang/system">\n            <config>\n               <domain-name>abc.xyz</domain-name>\n            </config>\n         </system>\n      </config></nc:edit-config></nc:rpc>\n##\n'

      #self.pattern_11 = re.compile('\n#232\n<?xml version="1.0" encoding="UTF-8"?><nc:rpc xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:8f46c033-b9c3-49e6-9ea8-900e427347da"><nc:get-config><nc:source><nc:running/></nc:source></nc:get-config></nc:rpc>\n##\n')


###################################################################################
#
# Gets the NETCONF message
#
###################################################################################
   def read_message(self):
      logging.debug("NCSocket - read_message")
      version = NC_BASE_1_0

      self.buffer = b''
#      while self.term_as_bytes not in self.buffer:
#      while any(self.term_as_bytes in self.buffer, 
      while not [t for t in self.terminators if t in self.buffer]:
#if any(item in 'cat' for item in ['a', 'd'])
         if self.sock.recv_ready():
            data = self.sock.recv(READ_SIZE)
            if not data:
               """Not read anything"""
               logging.debug("buffer:NO DATA")

            self.buffer += data
            logging.debug("buffer:" + str(self.buffer))

#      logging.debug("FINAL: buffer:" + str(self.buffer))

      request = self.buffer.decode()
      logging.debug("RAW: request:" + str(request))

      m10 = self.pattern_10.search(request)
      m11 = self.pattern_11.search(request)
      if m10:
         logging.debug("Message is 1.0 base")
         request = m10.group(1)
         logging.debug("Body=" + str(request))
      elif m11:
         logging.debug("Message is 1.1 base")
         size = m11.group(1)
         request = m11.group(2)
         logging.debug("Size=" + str(size))
         logging.debug("Body=" + str(request))
         logging.debug("len=" + str(len(request)))
         version = NC_BASE_1_1
      else:
         logging.debug("Message is unknown base"+ str(request))

      request = request.split(']]>]]>', 1)[0]
      request = request.strip()

      #request = request.replace(']]>]]>', '')
#      logging.debug("FINAL: request:" + request)
      return version,request

###################################################################################
#
# Writes the NETCONF base 1.0 message 
#
###################################################################################
   def write_message_1_0(self, message):
      self.sock.send(message)
      self.sock.send(NC_TERMINATOR_1_0)

###################################################################################
#
# Writes the NETCONF base 1.1 message 
#
###################################################################################
   def write_message_1_1(self, message):
      self.sock.send("\n#{}\n".format(len(message)))
      self.sock.send(message)
      self.sock.send(NC_TERMINATOR_1_1)

   

###################################################################################
#
# Close
#
###################################################################################
   def close(self):
      #self.sock.flush() 
      self.sock.close()

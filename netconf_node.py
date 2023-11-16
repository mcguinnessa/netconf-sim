
import logging
import xml.etree.ElementTree as ET
from xml import etree

from nc_socket import NCSocket
from netconf_subsys import NC_TERMINATOR


CLOSE_SESSION_TAG = "close-session"
COMMAND_TAG = "command"
HELLO_TAG = "hello"
RPC_TAG = "rpc"

GET_CONFIG_TAG = "get-config"


#NC_TERMINATOR = "]]>]]>"

"""This is the close request from the client"""
"""
   C: <?xml version="1.0" encoding="UTF-8"?>
   C: <rpc message-id="106"
   C: xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
   C:   <close-session/>
   C: </rpc>
   C: ]]>]]>

   S: <?xml version="1.0" encoding="UTF-8"?>
   S: <rpc-reply id="106"
   S: xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
   S:   <ok/>
   S: </rpc-reply>
   S: ]]>]]>
"""


class NETCONFTestNode():

   def __init__(self):
      logging.debug("NETCONFTestNode init")
      logging.debug("""<?xml version="1.0" encoding="UTF-8"?><rpc message-id="101"><get-config><source><running/></source><config xmlns="http://example.com/schema/1.2/config"><users/></config></get-config></rpc>]]>]]>""")
      logging.debug("""<?xml version="1.0" encoding="UTF-8"?><rpc message-id="106" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><close-session/></rpc>]]>]]>""")
      logging.debug("""<?xml version="1.0" encoding="UTF-8"?><hello><capabilities><capability>urn:ietf:params:xml:ns:netconf:base:1.0</capability></capabilities></hello>]]>]]>""")

      self.namespaces = {'base': 'urn:ietf:params:xml:ns:netconf:base:1.0'}
      self.CLOSED = False


###################################################################################
#
# The session loop
#
###################################################################################
   def handle_session(self, channel):
      logging.debug("NETCONFTestNode handle_session")

      sock = NCSocket(channel)

      channel.send(self.get_hello_resp())
      channel.send(NC_TERMINATOR)


      while not self.CLOSED:
         resp = None
         hello_el2 = None
         close_session_el = None
         command_el = None
         
         try:
            request = sock.read_message()
            #logging.debug("Request Type:" + str(type(request)))

            xmlroot = ET.fromstring(request)
            #logging.debug("xmlroot Type:" + str(type(xmlroot)))

            logging.debug("xmlroot:" + str(xmlroot))
            logging.debug("IN:" + ET.canonicalize(ET.tostring(xmlroot, encoding='utf8')))

            roottag_list = xmlroot.tag.split('}')
            roottag = roottag_list[-1]

            #logging.debug("roottag_list:" + str(roottag_list))
            #logging.debug("roottag_list len:" + str(len(roottag_list)))
            
            logging.debug("Root Tag:" + str(roottag))
            #logging.debug(RPC_TAG + "=" + str(roottag))
            #logging.debug("RPC_TAG Type:"+str(type(RPC_TAG)) + "=roottag:" + str(type(roottag)))
            #logging.debug("RPC_TAG Len:"+str(len(RPC_TAG)) + "=roottag:" + str(len(roottag)))

            if roottag == RPC_TAG:
               logging.debug("RPC Message")
               command_el = xmlroot.find(GET_CONFIG_TAG, self.namespaces)
               if command_el is not None:
                  logging.debug("get-config is found")
                  logging.debug("GET-CONFIG Message")
#                  command = command_el.text
#                  logging.debug("command:" + str(command))
#                  if command == "showConfig":
#                     logging.debug("showConfig recognised")
                  resp = self.get_show_data_resp()
                     #channel.send(data)
                     #channel.send(NC_TERMINATOR)

               #close_session_el = xmlroot.find('close-session', self.namespaces)
               close_session_el = xmlroot.find('base:'+CLOSE_SESSION_TAG, self.namespaces)
               if close_session_el is not None:
                  logging.debug("CLOSE-SESSION Message")
                  #logging.debug("close-session recognised")
                  resp = self.get_close_resp()
                  self.CLOSED = True

            elif roottag == HELLO_TAG:
               #logging.debug("Hello Message")
               #logging.debug("Message Root:" + str(ET.tostring(xmlroot, encoding='utf8')))
               #hello_el2 = xmlroot.findall(HELLO_TAG, self.namespaces)
               #hello_el2 = xmlroot.find(HELLO_TAG, self.namespaces)
               #if hello_el2 is not None and len(hello_el2) > 0:
               #if hello_el2 is not None:
               logging.debug("hello message - not responding")
               #logging.debug("->" + str(hello_el2))
               continue;

            else:
               logging.debug("Unrecognised tag:" + str(roottag))
       

         except Exception as e:
            import traceback
            print(traceback.format_exc())
            logging.info("Error handling message Database:" + str(e))

         if resp is None:
            print("Unrecognised command:" + str(request))
            resp = self.get_error_resp()

         logging.debug("OUT:" + ET.canonicalize(resp))
         channel.send(resp)
         channel.send(NC_TERMINATOR)


      sock.close()
            
#  <rpc message-id="101"><command>showConfig</command><params>None</params></rpc>]]>]]>
###################################################################################
#
# The RPC Response
#
###################################################################################
   def get_show_data_resp(self):
      data = """<rpc-reply xmlns="URN" xmlns:nokia="URL">
          <ok/>
        </rpc-reply>""" 
      return data

###################################################################################
#
# The Hello Response
#
###################################################################################
   def get_hello_resp(self):
      return """
         <hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
           <capabilities>
              <capability>urn:ieft:params:netconf:base:1.0</capability>
              <capability>urn:ieft:params:netconf:capability:candidate:1.0</capability>
              <capability>urn:ieft:params:netconf:capability:validate:1.0</capability>
              <capability>urn:ieft:params:netconf:capability:action:1.0</capability>
              <capability>urn:ieft:params:netconf:capability:notification:1.0</capability>
              <capability>urn:ieft:params:netconf:capability:interleave:1.0</capability>
              <capability>urn:ericsson:com:netconf:notification:1.1</capability>
              <capability>urn:ericsson:com:sgsnmme:heartbeat:1.0</capability>
              <capability>http://www.ericsson.com/gsn/4.0/contentVersion</capability>
              <capability>http://www.ericsson.com/gsn/3.0/protocolVersion</capability>
           </capabilities>
           <session-id>1</session-id>
         </hello> 
       """


###################################################################################
#
# The Error Response
#
###################################################################################
   def get_error_resp(self):
      return """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
         <rpc-error>
            <error-type>rpc</error-type>
            <error-tag>operation-failed</error-tag>
            <error-severity>error</error-severity>
         </rpc-error>
      </rpc-reply>
      """
#<?xml version="1.0" encoding="UTF-8"?><rpc message-id="106" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><close-session/></rpc>]]>]]>
###################################################################################
#
# The Close Response
#
###################################################################################
   def get_close_resp(self):
      return """<?xml version="1.0" encoding="UTF-8"?>
         <rpc-reply id="106"
            xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <ok/>
         </rpc-reply>"""


 



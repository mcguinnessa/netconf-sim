
import logging
import xml.etree.ElementTree as ET
from xml import etree

#from nc_socket import NCSocket
from nc_session import NCSession
from netconf_spec import *
from responses import Responses


#CLOSE_SESSION_TAG = "close-session"
HELLO_TAG = "hello"
ERROR_TAG = "error"
RPC_TAG = "rpc"




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

   def __init__(self, response_caching, server):
      logging.debug("NETCONFTestNode init")
      logging.debug("""<?xml version="1.0" encoding="UTF-8"?><rpc message-id="101"><get-config><source><running/></source><config xmlns="http://example.com/schema/1.2/config"><users/></config></get-config></rpc>]]>]]>""")
      logging.debug("""<?xml version="1.0" encoding="UTF-8"?><rpc message-id="106" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><close-session/></rpc>]]>]]>""")
      logging.debug("""<?xml version="1.0" encoding="UTF-8"?><hello><capabilities><capability>urn:ietf:params:xml:ns:netconf:base:1.0</capability></capabilities></hello>]]>]]>""")

      self.namespaces = {'' : '', 'base': 'urn:ietf:params:xml:ns:netconf:base:1.0', 'nc' : 'urn:ietf:params:xml:ns:netconf:base:1.0'}
      self.CLOSED = False
      #self.terminator = NC_TERMINATOR_1_0
      self.server = server

      self.responses = Responses("./responses", response_caching)


###################################################################################
#
# The session loop
#
###################################################################################
   def handle_session(self, channel):
      logging.debug("NETCONFTestNode handle_session")

      session = NCSession(channel)

      hello_resp = self.responses.get_response_for(HELLO_TAG)
      logging.info("OUT:" + ET.canonicalize(hello_resp))
      session.write_message(hello_resp)
#      channel.send(hello_resp)
#      channel.send(NC_TERMINATOR_1_0)
      logging.info("Sent Hello message to client")

      while not self.CLOSED:
         logging.debug("Waiting for data.")
         resp = None
         #hello_el2 = None
         close_session_el = None
         command_el = None
         mid = ""
         
         try:
            request = session.read_message()
            #logging.debug("Request Type:" + str(type(request)))

            xmlroot = ET.fromstring(request)
            #logging.info("IN:" + ET.canonicalize(xmlroot))

            logging.debug("xmlroot:" + str(xmlroot))
            logging.info("IN:" + ET.canonicalize(ET.tostring(xmlroot, encoding='utf8')))

            roottag_list = xmlroot.tag.split('}')
            roottag = roottag_list[-1]

            
            logging.debug("Root Tag:" + str(roottag))
            if roottag == RPC_TAG:
               logging.debug("RPC Message")

               mid = xmlroot.attrib['message-id']
               logging.debug("mid:" + str(mid))

               tag = xmlroot[0].tag.split("}",1)[-1]
               logging.debug("   TAG:" + str(tag))

               if tag == CLOSE_SESSION_TAG:
                  self.CLOSED = True

               resp = self.responses.get_response_for(tag)
               logging.debug("   BODY(raw):" + str(resp))
               if "{}" in resp:
                  resp = resp.format(mid)
                  logging.debug("   BODY(formatted):" + str(resp))
          
            elif roottag == HELLO_TAG:
               logging.debug("hello message - not responding")
               continue;

            else:
               logging.info("Unrecognised tag:" + str(roottag))
       

         except Exception as e:
            import traceback
            print(traceback.format_exc())
            logging.info("Error handling message:" + str(e))

         if resp is None:
            logging.debug("Unrecognised command:" + str(request))
            #resp = self.get_error_resp(mid)
            resp = self.responses.get_response_for(ERROR_TAG)

         #logging.debug(resp)
         #logging.info("OUT:" + ET.canonicalize(resp))
         #channel.send(resp)
         session.write_message(resp)

      #sock.close()
      session.close()
      self.server.event.set()
            
#  <rpc message-id="101"><command>showConfig</command><params>None</params></rpc>]]>]]>
###################################################################################
#
# The RPC Response
#
###################################################################################
#   def get_config_resp(self, mid):
#      return """<?xml version="1.0" encoding="UTF-8"?>
#         <rpc-reply message-id="{}" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
#             <data>
#                 <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf" xmlns:nokia-attr="urn:nokia.com:sros:ns:yang:sr:attributes">
#                     <system>
#                         <name nokia-attr:comment="This is a comment on the system name."> node2</name>
#                     </system>
#                 </configure>
#             </data>
#         </rpc-reply>
#      """.format(mid)
###################################################################################
#
# The RPC Response
#
###################################################################################
#   def get_config_resp_example(self, mid):
##      data = """<rpc-reply xmlns="URN" xmlns:nokia="URL" message-id="{}">
##          <ok/>
##        </rpc-reply>""".format(mid)
##      return data
#
#
##	<?xml version="1.0" encoding="UTF-8"?>
#
#      return """
#         <rpc-reply message-id="{}">
#            <data>
#               <native xmlns="http://cisco.com/yang/namespace">
#                  <version>10.5</version>
#                  <boot-start-marker></boot-start-marker>
#                  <boot-end-marker></boot-end-marker>
#                  <service>
#                     <timestamps>
#                        <debug>
#                           <datetime>
#                              <msec></msec>
#                           </datetime>
#                        </debug>
#                        <log>
#                           <datetime>
#                              <msec></msec>
#                           </datetime>
#                        </log>
#                     </timestamps>
#                  </service>
#                  <platform>
#                     <console xmlns="http://nokia.com/yang/myyang">
#                           <output>serial</output>
#                     </console>
#                  </platform>
#                  <hostname>raspberrypi</hostname>
#                  <enable>
#                     <password>
#                        <secret>secretword</secret>
#                     </password>
#                  </enable>
#               </native>
#            </data>
#        </rpc-reply>""".format(mid)

###################################################################################
#
# The Hello Response
#
###################################################################################
#   def get_hello_resp(self):
#      return """
#         <hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
#           <capabilities>
#              <capability>urn:ieft:params:netconf:base:1.0</capability>
#              <capability>urn:ieft:params:netconf:capability:candidate:1.0</capability>
#              <capability>urn:ieft:params:netconf:capability:validate:1.0</capability>
#              <capability>urn:ieft:params:netconf:capability:action:1.0</capability>
#              <capability>urn:ieft:params:netconf:capability:notification:1.0</capability>
#              <capability>urn:ieft:params:netconf:capability:interleave:1.0</capability>
#              <capability>urn:ericsson:com:netconf:notification:1.1</capability>
#              <capability>urn:ericsson:com:sgsnmme:heartbeat:1.0</capability>
#              <capability>http://www.ericsson.com/gsn/4.0/contentVersion</capability>
#              <capability>http://www.ericsson.com/gsn/3.0/protocolVersion</capability>
#           </capabilities>
#           <session-id>1</session-id>
#         </hello> 
#       """


###################################################################################
#
# The Error Response
#
###################################################################################
#   def get_error_resp(self, mid):
#      #return """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="106">
#      return """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="{}">
#         <error>
#            <error-type>rpc</error-type>
#            <error-tag>operation-failed</error-tag>
#            <error-severity>error</error-severity>
#         </error>
#      </rpc-reply>
#      """.format(mid)
##<?xml version="1.0" encoding="UTF-8"?><rpc message-id="106" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><close-session/></rpc>]]>]]>
###################################################################################
#
# The Close Response
#
###################################################################################
#   def get_close_resp(self, mid):
#      return """<?xml version="1.0" encoding="UTF-8"?>
#         <rpc-reply message-id="{}"
#            xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
#            <ok/>
#         </rpc-reply>""".format(mid)
#

 



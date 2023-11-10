
import xml.etree.ElementTree as ET


class NETCONFTestNode():

   hello_sent = False

   def __init__(self):
      print("NETCONFTestNode init")


   def handle_session(self, channel):
      print("NETCONFTestNode handle_session")

      if not self.hello_sent:
         data = self.get_hello_resp()
         channel.send(data)
         self.hello_sent = True

      while True:
         if channel.recv_ready():
            buf = channel.recv(100)
            print("buf:" + str(buf))

            xmlroot = ET.fromstring(buf)
            #cmd = str(buf).strip()
            #cmd = str(buf.strip())
            print("xmlroot:" + str(xmlroot))

            command = str(xmlroot.find('command').text)
            print("command:" + str(command))
            
            if command == "showConfig":
               print("showConfig recognised")
               data = self.get_show_data_resp()
               channel.send(data)
            else:
               print("Unrecognised command:" + str(show-data))
            

      #data = "ALEX LIVERPOOL"

#  <rpc><command>showConfig</command></rpc>

   def get_show_data_resp(self):
      data = """<rpc-reply xmlns="URN" xmlns:nokia="URL">
          <ok/>
        </rpc-reply>]]>]]>""" 
      return data




 
   def get_hello_resp(self):
      data = """<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">    
    <capabilities>
        <capability>urn:ietf:params:netconf:base:1.0</capability>
        <capability>urn:ietf:params:netconf:base:1.1</capability>
        <capability>urn:ietf:params:netconf:capability:writable-running:1.0</capability>
        <capability>urn:ietf:params:netconf:capability:validate:1.0</capability>
        <capability>urn:ietf:params:netconf:capability:validate:1.1</capability>
        <capability>urn:ietf:params:netconf:capability:startup:1.0</capability>
        <capability>urn:ietf:params:netconf:capability:url:1.0?scheme=ftp,tftp,file</ capability>
        <capability>urn:ietf:params:netconf:capability:with-defaults:1.0?basicmode=trim</capability>
        <capability>urn:ietf:params:xml:ns:netconf:base:1.0?module=ietf-netconf&amp;revision=2015-02-27&amp;features=writable-running,validate,startup,url&amp;deviations=alu-netconf-deviations-r13</capability>
        <capability>urn:xxx-network.com:sros:ns:yang:netconf-deviations-r13?module= xxx-network -deviations-r13&amp;revision=2015-02-27</capability>
        <capability>urn:xxx-network.com:sros:ns:yang:cli-content-layer-r13?module= xxx-network -cli-content-layer-r13&amp;revision=2015-02-27</capability>
        <capability>urn:xxx-network.com:sros:ns:yang:conf-r13?module=confr13&amp;revision=2015-02-27</capability>
        <capability>urn:xxx-network.com:sros:ns:yang:conf-aaa-r13?module=conf-aaar13&amp;revision=2015-02-27</capability>
        <capability>urn:xxx-network.com:sros:ns:yang:conf-vsm-r13?module=conf-vsmr13&amp;revision=2015-02-27</capability>
    </capabilities>
    <session-id>54</session-id>
</hello>
    ]]>]]>"""
      return data
    




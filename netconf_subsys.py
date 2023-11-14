# Based on demo_server.py from the Paramiko package
#
# Copyright (C) 2003-2007  Robey Pointer <*****@*****.**>
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.

from paramiko.server import SubsystemHandler
#from parrot_log import Logger
import logging


NETCONF_PORT=830
NC_TERMINATOR = "]]>]]>"



class NETCONFsubsys(SubsystemHandler):
    cb_target = None

    @staticmethod
    def register_callback_object(cb_target):
        logging.debug("Registering callback object")
        NETCONFsubsys.cb_target = cb_target
        logging.debug('NETCONFsubsys: registered cb={cb_target}'.format(cb_target=str(cb_target)))

    def __init__(self, channel, name, server, *largs, **kwargs):
        logging.debug("NETCONFsubsys: init channel={channel} name={name} server={server}".format(channel=str(channel), server=str(server), name=str(name)))
        SubsystemHandler.__init__(self, channel, name, server)
        transport = channel.get_transport()
        self.ultra_debug = transport.get_hexdump()
        self.next_handle = 1
        logging.debug("NETCONFsubsys: init done")

    def start_subsystem(self, name, transport, channel):
        logging.debug("NETCONFsubsys: start_subsystem name={name} transport={transport} channel={channel}".format(name=str(name), transport=str(transport), channel=str(channel)))
        self.sock = channel
        logging.debug("Started NETCONF server on channel {!r}".format(channel))
        try:
            self.handle_session()
        except Exception as e:
           logging.debug("NETCONFsubsys: callback exception:" + str(e))
           import traceback
           traceback.print_exc()
           logging.debug("Stopped NETCONF server on channel {!r}'.format(channel)")

    def finish_subsystem(self):
        logging.debug('NETCONFsubsys: finish_subsystem')
        threading.current_thread().daemon = True
        self.server.session_ended()
        logging.debug("NETCONF subsys finished")
        super(NETCONFsubsys, self).finish_subsystem()
        logging.debug("NETCONF subsys finished 2")
        logging.debug("NETCONF subsys finished 3")

    def handle_session(self):
       logging.debug("NETCONF subsys session started")

#       data = "ALEX LIVERPOOL"
#       self.sock.send(data) 
      
       NETCONFsubsys.cb_target.handle_session(self.sock)
       logging.debug("NETCONF subsys session ended")

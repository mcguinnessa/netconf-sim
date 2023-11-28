import logging
import os


#RESPONSE_DIR = "./responses"


class Responses():

    response_map = {}

    def __init__(self, response_path, caching):
        logging.debug("Init Responses with " + response_path)
        self.caching = not caching
        self.populate(response_path)

####################################################################################
#
# Populate the map
#
####################################################################################
    def populate(self, response_path):

        if os.path.exists(response_path) and os.path.isdir(response_path) :
           logging.debug(response_path + " exists")

           for (dirpath, dirnames, filenames) in os.walk(response_path):
              logging.debug("Files:" + str(filenames))

              files = [ fi for fi in filenames if fi.endswith(".xml")]
              for filename in files:
                 with open(os.path.join(dirpath,filename)) as f:
                    payload = f.read()
 
                    name_suffix = filename.split(".")
                    logging.info("Found response for - " + str(name_suffix[0]))
                    logging.debug("NAME:" + str(name_suffix[0]))
                    logging.debug("BODY:" + str(payload))
                    self.response_map[name_suffix[0]] = payload.strip()

              break

        logging.debug("Response Map:" + str(self.response_map))

####################################################################################
#
# Get a response for a given command
#
####################################################################################
    def get_response_for(self, command_name):

       logging.debug("Caching:" + str(self.caching))
       rc = ""
       if command_name in self.response_map.keys():
          rc = self.response_map[command_name]

       return rc
       

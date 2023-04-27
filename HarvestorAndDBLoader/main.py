# Assignment 2 - COMP90024 Course at The University of Melbourne

import re
import time
import os
from db_gateway import Couch



couchdb_master_ip='localhost'
# Inctance of couchdb connection class


couch=Couch('http://'+couchdb_master_ip+':5984/',['toot'])


# Fetching toots

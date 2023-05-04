# Assignment 2 - COMP90024-A2 Course at The University of Melbourne

import requests
import json
import couchdb
from db_gateway import Couch



couchdb_master_ip='localhost'
# Inctance of couchdb connection class


couch=Couch('http://'+couchdb_master_ip+':5984/',['toot'])


# Fetching toots



# Set up Mastodon API credentials
mastodon_instance = "https://mastodon.social"
access_token = "N4L6SX4so4lbcMB8x2CNJASQPbdFXBLE4wMYC1J6W34"

# Set up CouchDB connection


# Set up stream filters
keywords = ["Rent", "Interest Rate", "RBA"]
stream_url = f"{mastodon_instance}/api/v1/streaming/user"
params = {
    "access_token": access_token,
    "stream": "public",
    "timeout": "20",
    "filter": ",".join(keywords)
}

# Set up stream connection
response = requests.get(stream_url, params=params, stream=True)

# Read stream data and store in CouchDB
for line in response.iter_lines():
    if line:
        try:
            data = json.loads(line)
            couch.pushdata(data,'toot')
        except Exception as e:
            print(f"Error parsing JSON: {e}")

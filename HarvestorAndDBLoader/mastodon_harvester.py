
from mastodon import Mastodon, MastodonNotFoundError
import requests
from requests.auth import HTTPBasicAuth
import datetime as dt
import pandas as pd
import re
from io import StringIO
from html.parser import HTMLParser
from textblob import TextBlob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--ado_api_key", help="api key for ado server")
parser.add_argument("--ado_login_url", help="ado api login url")
parser.add_argument("--ado_text_search_mastodon_url", help="ado api text search url for mastodon")
parser.add_argument("--mastodon_api_key", help="api key for the mastodon server")
parser.add_argument("--couchdb_ip", help="ip address of the couchdb server")
args = parser.parse_args()


ADO_API_KEY = args.ado_api_key
ADO_LOGIN_URL = args.ado_login_url
ADO_TEXT_SEARCH_URL = args.ado_text_search_mastodon_url
MASTODON_KEY = args.mastodon_api_key

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


# Login to ADO

res = requests.post(ADO_LOGIN_URL, auth=HTTPBasicAuth('apikey', ADO_API_KEY))
if res.ok:
    jwt = res.text



# Generate ADO query

text_kws = ['interest rate', ' rba', 'rba decision', "rba's decision",
            'cash rate', 'interest payment', 'interest repayment', 'interest re-payment', 'repayment of interest',
            'variable interest', 'fixed interest', 'bank interest', 'rate hike',
            'mortgage', 'rent payment', 'house rent', 'houserent', 'house payment', 'housing',
            'inflation', 'cpi index', 'cost of living', 'shrinkflation',
            'social security', 'job seeker', 'jobseeker', 'youth allowance', 'austudy', 'centrelink', 'centerlink']
look_back_days = 7

today = dt.datetime.now().date()
text_kws = [f'text:"{kw}"' for kw in text_kws]
dates = [f"""date:\"{date.strftime('%Y%m%d')}\"""" for date in pd.date_range(today-dt.timedelta(days=look_back_days), today)]

query = '('+' OR '.join(text_kws) +') AND (' + ' OR '.join(dates) + ')'



# Retrivie post ids - this takes around 1 min

qs_params = { 'query' : query}
headers = {'Authorization': f"Bearer {jwt}"}
res = requests.get(ADO_TEXT_SEARCH_URL, headers = headers, params=qs_params)
result = res.json()

while True: #each API request returns 200 ids, need multiple requests in order to get all toots
    headers = {'Authorization': f"Bearer {jwt}", 'x-ado-bookmark':res.headers['x-ado-bookmark']}
    res = requests.get(ADO_TEXT_SEARCH_URL, headers = headers, params=qs_params)
    result_2 = res.json()
    if result_2 == []:
        break
    result.extend(result_2)

#Retrive toots from Mastodon API

sentiments = []

for line in result[:100]: #capping the number of toots to display (for now)
    id = line.split('/')
    try:
        toot = Mastodon(api_base_url=f'https://{id[0]}',
                        access_token = MASTODON_KEY).status(id[2])['content']
        toot_clean = strip_tags(toot)
        sentiment = TextBlob(toot_clean).sentiment.polarity
        print("Sentiment: ",sentiment)
        sentiments.append(sentiment)
    except:
        print("Error getting the toot") #TO DO: REMOVE PRINT
        continue

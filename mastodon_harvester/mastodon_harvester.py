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
import time
import sys
import os
import json

# Get the parent directory of the current directory
parent_dir = os.path.dirname(os.path.abspath(__file__))
# Append the parent directory to the system path
sys.path.append(os.path.join(parent_dir, "..", "flask_api"))

from harvester import FetcherHarverster


# Now you can use the Fetcher class


# parser = argparse.ArgumentParser()
# parser.add_argument(
#     "--ado_api_key",
#     help="api key for ado server",
#     default="a2a6e2f96a2c94a04661aacc6e394caa",
# )
# parser.add_argument(
#     "--ado_login_url",
#     help="ado api login url",
#     default="https://api.ado.eresearch.unimelb.edu.au/login",
# )
# parser.add_argument(
#     "--ado_text_search_mastodon_url",
#     help="ado api text search url for mastodon",
#     default="https://api.ado.eresearch.unimelb.edu.au/analysis/textsearch/collections/mastodon",
# )
# parser.add_argument(
#     "--mastodon_api_key",
#     help="api key for the mastodon server",
#     default="f8-yNpSEGxPcQwwz_GxYtET3VumoGZ6KAQAH6bybICE",
# )
# args = parser.parse_args()


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
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
class Process_Mastodon:
    def __init__(
        self, ADO_API_KEY, ADO_LOGIN_URL, ADO_TEXT_SEARCH_URL, MASTODON_KEY
    ) -> None:
        self.ADO_API_KEY = ADO_API_KEY  #'a2a6e2f96a2c94a04661aacc6e394caa'
        self.ADO_LOGIN_URL = (
            ADO_LOGIN_URL  #'https://api.ado.eresearch.unimelb.edu.au/login'
        )
        self.ADO_TEXT_SEARCH_URL = ADO_TEXT_SEARCH_URL  #'https://api.ado.eresearch.unimelb.edu.au/analysis/textsearch/collections/mastodon'
        self.MASTODON_KEY = MASTODON_KEY  #'f8-yNpSEGxPcQwwz_GxYtET3VumoGZ6KAQAH6bybICE'

    # Helper function to clean toots from HTML tags
    def get_Toots(self):
        res = requests.post(
            self.ADO_LOGIN_URL, auth=HTTPBasicAuth("apikey", self.ADO_API_KEY)
        )
        if res.ok:
            jwt = res.text

        # Generate ADO query

        text_kws = [
            "interest rate",
            " rba",
            "rba decision",
            "rba's decision",
            "cash rate",
            "interest payment",
            "interest repayment",
            "interest re-payment",
            "repayment of interest",
            "variable interest",
            "fixed interest",
            "bank interest",
            "rate hike",
            "mortgage",
            "rent payment",
            "house rent",
            "houserent",
            "house payment",
            "housing",
            "inflation",
            "cpi index",
            "cost of living",
            "shrinkflation",
            "social security",
            "job seeker",
            "jobseeker",
            "youth allowance",
            "austudy",
            "centrelink",
            "centerlink",
        ]
        look_back_days = 7

        today = dt.datetime.now().date()
        text_kws = [f'text:"{kw}"' for kw in text_kws]
        dates = [
            f"""date:\"{date.strftime('%Y%m%d')}\""""
            for date in pd.date_range(today - dt.timedelta(days=look_back_days), today)
        ]

        query = "(" + " OR ".join(text_kws) + ") AND (" + " OR ".join(dates) + ")"

        # Retrivie post ids - this takes around 1 min

        qs_params = {"query": query}
        headers = {"Authorization": f"Bearer {jwt}"}
        res = requests.get(self.ADO_TEXT_SEARCH_URL, headers=headers, params=qs_params)
        result = res.json()

        while (
            True
        ):  # each API request returns 200 ids, need multiple requests in order to get all toots
            headers = {
                "Authorization": f"Bearer {jwt}",
                "x-ado-bookmark": res.headers["x-ado-bookmark"],
            }
            res = requests.get(
                self.ADO_TEXT_SEARCH_URL, headers=headers, params=qs_params
            )
            result_2 = res.json()
            if result_2 == []:
                break
            result.extend(result_2)
        return result


# Retrive toots from Mastodon API & send to CouchDB


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Harvest Mastodon"
    )  # FIXME: Better description
    parser.add_argument(
        "--couchdb_master_ip",
        type=str,
        help="ip of a node in the couchdb cluster",
        default="localhost",
    )
    parser.add_argument(
        "--couchdb_username",
        type=str,
        help="username of the couchdb cluster",
        default="admin",
    )
    parser.add_argument(
        "--couchdb_password",
        type=str,
        help="password of the couchdb cluster",
        default="admin",
    )
    parser.add_argument(
        "--ado_api_key",
        help="api key for ado server",
        default="a2a6e2f96a2c94a04661aacc6e394caa",
    )
    parser.add_argument(
        "--ado_login_url",
        help="ado api login url",
        default="https://api.ado.eresearch.unimelb.edu.au/login",
    )
    parser.add_argument(
        "--ado_text_search_mastodon_url",
        help="ado api text search url for mastodon",
        default="https://api.ado.eresearch.unimelb.edu.au/analysis/textsearch/collections/mastodon",
    )
    parser.add_argument(
        "--mastodon_api_key",
        help="api key for the mastodon server",
        default="f8-yNpSEGxPcQwwz_GxYtET3VumoGZ6KAQAH6bybICE",
    )

    args = parser.parse_args()
    process = Process_Mastodon(
        args.ado_api_key,
        args.ado_login_url,
        args.ado_text_search_mastodon_url,
        args.mastodon_api_key,
    )
    fetcher2 = FetcherHarverster(
        args.couchdb_master_ip, args.couchdb_username, args.couchdb_password
    )

    result = process.get_Toots()
    for i in result:
        id = i.split("/")
        try:
            toot = Mastodon(
                api_base_url=f"https://{id[0]}", access_token=args.mastodon_api_key
            ).status(id[2])["content"]
            toot_clean = strip_tags(toot)
            sentiment = TextBlob(toot_clean).sentiment.polarity
            sentiment = {"sentiment": sentiment}
            sentiment = json.dumps(sentiment)
            fetcher2.harvestAndPush(sentiment)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            continue

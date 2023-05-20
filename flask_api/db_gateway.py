#
import couchdb
import json
import time
import random
import requests
import os


class Couch:
    # Establishing Connection with db
    def __init__(
        self, ip, dbnamelist, username: str = "admin", password: str = "admin"
    ):
        couchserver = couchdb.Server(url=ip)
        couchserver.resource.credentials = (username, password)
        # Variable to store database objects
        self.db = []
        # Pre requisite db
        dbsl = dbnamelist
        couchdb_master_ip = "localhost"
        # couchdb_master_login_url = "http://admin:admin@" + couchdb_master_ip + ":5984/"
        # Reading other node ip to enable replication

        # Creating or loading db
        for dbname in dbsl:
            self.db = self.db + [self.createdb(couchserver, dbname)]
        for dbname in dbnamelist:
            self.db = self.db + [self.createdb(couchserver, dbname)]
        # Adding static data to db
        self.create_static()

    # Creating db if it does not exist, else loading it
    def createdb(self, couchserver, dbname):
        if dbname in couchserver:
            del couchserver[dbname]  # delete existing database
            return couchserver.create(dbname)
        else:
            return couchserver.create(dbname)
    # Adding static data to db needed by harvestor

    def create_static(self):
        wordir = os.getcwd()
        twitter_file = f'{wordir}/data/twitter/twitter_small.json'

        a = open(twitter_file)
        for i in a.readlines():
            t = json.loads(i)
            try:
                self.pushdata(t, "tweet")
            except Exception as e:
                print(f"An error occurred: {e}")

        rba_target_cash_rate_file = f'{wordir}/data/other/rba_target_cash_rate.json'
        a = open(rba_target_cash_rate_file)
        for i in a.readlines():
            t = json.loads(i)
            try:
                self.pushdata(t, "rba_target_cash_rate")
            except Exception as e:
                print(f"An error occurred: {e}")

        sudo_gccsa_income_mortgage_rent_file = f'{wordir}/data/other/sudo_gccsa_income_mortgage_rent_avg_2016.json'
        a = open(sudo_gccsa_income_mortgage_rent_file)
        for i in a.readlines():
            t = json.loads(i)
            try:
                self.pushdata(t, "sudo_gccsa_income_mortgage_rent_avg_2016")
            except Exception as e:
                print(f"An error occurred: {e}")

        sudo_gccsa_inequality_file = f'{wordir}/data/other/sudo_gccsa_inequality_2017.json'
        a = open(sudo_gccsa_inequality_file)
        for i in a.readlines():
            t = json.loads(i)
            try:
                self.pushdata(t, "sudo_gccsa_inequality_2017")
            except Exception as e:
                print(f"An error occurred: {e}")

        sudo_gccsa_housing_totals_file = f'{wordir}/data/other/sudo_gccsa_housing_totals_2016.json'
        a = open(sudo_gccsa_housing_totals_file)
        for i in a.readlines():
            t = json.loads(i)
            try:
                self.pushdata(t, "sudo_gccsa_housing_totals_2016")
            except Exception as e:
                print(f"An error occurred: {e}")

        inflation_file = f'{wordir}/data/other/inflation.json'
        a = open(inflation_file)
        for i in a.readlines():
            t = json.loads(i)
            try:
                self.pushdata(t, "inflation")
            except Exception as e:
                print(f"An error occurred: {e}")

    # Pushing harvested mastadon's toots
    def pushdata(self, data, dbname):
        flag = 0
        for i in self.db:
            if dbname == i._name:
                flag = 0
                i.save(data)
                break
            else:
                flag = 1
        if flag == 1:
            print(dbname + " does not exist")

# Test


def harvestAndPush():
    # Fetching toots
    while True:
        # To store toots
        all_toots = []  # I assume your streaming api is here
        # search_query = ''
        try:
            all_toots = []
            # Pushing toots to db
            for i in all_toots:
                couchdb.pushdata(i, "toot")
                print(i)

        except:
            pass

        del all_toots
        # print("--- %s seconds ---" % (time.time() - start_time))
        time.sleep(45)


def purge_database(database_url, database_name):
    # Connect to CouchDB server
    couch = couchdb.Server(database_url)

    try:
        # Check if the database exists
        if database_name in couch:
            # Access the specified database
            db = couch[database_name]

            # Get all the document IDs
            all_docs = [row.id for row in db.view('_all_docs')]

            # Purge all the documents
            for doc_id in all_docs:
                doc = db.get(doc_id)
                db.purge([doc])

            print("Database purged successfully.")

        else:
            print("Database does not exist.")

    except couchdb.ResourceNotFound:
        print("Database not found.")
    except Exception as e:
        print("An error occurred:", str(e))

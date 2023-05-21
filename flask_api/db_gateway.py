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
        if os.name == 'nt':  # Check if the operating system is Windows
            twitter_file = os.path.join(wordir, 'flask_api','data', 'twitter', 'twitter_small.json')
        else:  # Assume it's a Unix-like system (e.g., Linux or macOS)
            twitter_file = f'{wordir}/data/twitter/twitter_small.json'

        a = open(twitter_file)
        for i in a.readlines():
            t = json.loads(i)
            try:
                self.pushdata(t, "tweet")
            except Exception as e:
                print(f"An error occurred: {e}")
        if os.name == 'nt':  # Check if the operating system is Windows
            rba_target_cash_rate_file = f'{wordir}/flask_api/data/other/rba_target_cash_rate.json'
        else:  # Assume it's a Unix-like system (e.g., Linux or macOS)
            rba_target_cash_rate_file = f'{wordir}/data/other/rba_target_cash_rate.json'

        a = open(rba_target_cash_rate_file)
        for i in a.readlines():
            t = json.loads(i)
            try:
                self.pushdata(t, "rba_target_cash_rate")
            except Exception as e:
                print(f"An error occurred: {e}")
        if os.name == 'nt':  # Check if the operating system is Windows
            sudo_gccsa_income_mortgage_rent_file = f'{wordir}/flask_api/data/other/sudo_gccsa_income_mortgage_rent_avg_2016.json'
        else:  # Assume it's a Unix-like system (e.g., Linux or macOS)
            sudo_gccsa_income_mortgage_rent_file = f'{wordir}/data/other/sudo_gccsa_income_mortgage_rent_avg_2016.json'

        a = open(sudo_gccsa_income_mortgage_rent_file)

        for i in a.readlines():
            t = json.loads(i)
            try:
                self.pushdata(t, "sudo_gccsa_income_mortgage_rent_avg_2016")
            except Exception as e:
                print(f"An error occurred: {e}")
        if os.name == 'nt':  # Check if the operating system is Windows
             sudo_gccsa_inequality_file = f'{wordir}/flask_api/data/other/sudo_gccsa_inequality_2017.json'
        else:  # Assume it's a Unix-
            sudo_gccsa_inequality_file = f'{wordir}/data/other/sudo_gccsa_inequality_2017.json'

        a = open(sudo_gccsa_inequality_file)

        for i in a.readlines():
            t = json.loads(i)
            try:
                self.pushdata(t, "sudo_gccsa_inequality_2017")
            except Exception as e:
                print(f"An error occurred: {e}")
        if os.name == 'nt':  # Check if the operating system is Windows
            sudo_gccsa_housing_totals_file = f'{wordir}/flask_api/data/other/sudo_gccsa_housing_totals_2016.json'
        else:  # Assume it's a Unix-
            sudo_gccsa_housing_totals_file = f'{wordir}/data/other/sudo_gccsa_housing_totals_2016.json'

        a = open(sudo_gccsa_housing_totals_file)
        for i in a.readlines():
            t = json.loads(i)
            try:
                self.pushdata(t, "sudo_gccsa_housing_totals_2016")
            except Exception as e:
                print(f"An error occurred: {e}")

        if os.name == 'nt':  # Check if the operating system is Windows
            inflation_file = f'{wordir}/flask_api/data/other/inflation.json'
        else:  # Assume it's a Unix-
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

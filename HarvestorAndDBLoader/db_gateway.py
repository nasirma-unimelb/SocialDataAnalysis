
#
import couchdb
import json
import time
import random

class Couch:
    # Establishing Connection with db
    def __init__(self,ip,dbnamelist):
        couchserver=couchdb.Server(url=ip)
        couchserver.resource.credentials=('admin','admin')
        # Variable to store database objects
        self.db=[]
        # Pre requisite db
        dbsl=['interest_rates','inflation','tweet']
        couchdb_master_ip='localhost'
        couchdb_master_login_url='http://admin:admin@'+couchdb_master_ip+':5984/'
        # Reading other node ip to enable replication
     
        # Creating or loading db
        for dbname in dbsl:
            self.db=self.db+[self.createdb(couchserver,dbname)]
        for dbname in dbnamelist:
            self.db=self.db+[self.createdb(couchserver,dbname)]
        # Adding static data to db
        self.create_static()

    # Creating db if it does not exist, else loading it
    def createdb(self,couchserver,dbname):
        if dbname in couchserver:
            return couchserver[dbname]
        else:
            return couchserver.create(dbname)

    # Adding static data to db needed by harvestor
    def create_static(self):
        a=open('data/other/inflation.json')
        for i in a.readlines():
            c=json.loads(i)
            try:
                self.pushdata(c,'inflation')
            except:
                pass
        a=open('data/other/interest_rates.json')
        for i in a.readlines():
            d=json.loads(i)
            try:
                self.pushdata(d,'interest_rates')
            except:
                pass

        a=open('data/twitter/twitter_small.json')
        for i in a.readlines():
            t=json.loads(i)
            try:
                self.pushdata(t,'tweet')
            except Exception as e:
             print(f"An error occurred: {e}")

    # Pushing harvested mastadon's toots
    def pushdata(self,data,dbname):
        flag=0
        for i in self.db:
            if dbname==i._name:
                flag=0
                i.save(data)
                break
            else:
                flag=1
        if flag==1:
            print(dbname+" does not exist")

import couchdb
import json
from db_gateway import Couch
import os


class FetcherHarverster:
    def __init__(self, couchdb_master_ip, couchdb_username, couchdb_password) -> None:
        # Connect to the CouchDB server and select a database
      
       
        dbsl = [
            # "tweet",
            # "rba_target_cash_rate",
            # "sudo_gccsa_income_mortgage_rent_avg_2016",
            # "sudo_gccsa_housing_totals_2016",
            # "sudo_gccsa_inequality_2017",
            # "inflation",
                "toot",
        ]
        self.view_name_toot = "toot_Data"
        self.design_doc_name_toot = "_design/mydesign_" + self.view_name_toot

        self.couchobj = Couch(
            f"http://{couchdb_username}:{couchdb_password}@{couchdb_master_ip}:5984/", dbsl, couchdb_username, couchdb_password,True)

        self.couchdbs = couchdb.Server(
            f"http://{couchdb_username}:{couchdb_password}@{couchdb_master_ip}:5984/"
        )
       
        self.toot_db = self.couchdbs["toot"]


      # ---------toot View------------------------------------------------------------------------
    def get_toot(self):
        self.view_name_toot = "toot_Data"
        self.design_doc_name_toot = "_design/mydesign_" + self.view_name_toot

        # Define the map function
        toot_func = """
        function(doc) {
            var sentiment = doc.sentiment;
            var bin = '';

            if (sentiment < -1) {
                bin = '-1<';
            } else if (sentiment >= -1 && sentiment < -0.75) {
                bin = '-1 / -0.75';
            } else if (sentiment >= -0.75 && sentiment < -0.5) {
                bin = '-0.75 / -0.50';
            } else if (sentiment >= -0.5 && sentiment < -0.25) {
                bin = '-0.50 / -0.25';
            } else if (sentiment >= -0.25 && sentiment < 0) {
                bin = '-0.25 / 0.00';
            } else if (sentiment >= 0 && sentiment < 0.25) {
                bin = '0.00 / 0.25';
            } else if (sentiment >= 0.25 && sentiment < 0.50) {
                bin = '0.25 / 0.50';
            } else if (sentiment >= 0.50 && sentiment < 0.75) {
                bin = '0.50 / 0.75';
            } else if (sentiment >= 0.75 && sentiment <= 1) {
                bin = '0.75 / 1';
            } else if (sentiment > 1) {
                bin = '>1';
            }

            emit(bin, 1);
        }
        """

        # Define the reduce function
        toot_reduce_func = "_sum"

        # Define the design document name and view name
        design_doc_name = self.design_doc_name_toot
        view_name = self.view_name_toot

        # Check if the design document already exists
        if design_doc_name not in self.toot_db:
            self.toot_db.save({
                "_id": design_doc_name,
                "views": {
                    view_name: {
                        "map": toot_func,
                        "reduce": toot_reduce_func
                    }
                }
            })
        else:
            design_doc = self.toot_db[design_doc_name]
            if view_name not in design_doc.get("views", {}):
                design_doc["views"][view_name] = {
                    "map": toot_func,
                    "reduce": toot_reduce_func
                }
                self.toot_db.save(design_doc)


    # -----------------------END toot---------------------------------------------


   


    def save_toot_data(
        self,
    ):
        self.get_toot()
        result_toots = self.toot_db.view(
            self.design_doc_name_toot + "/_view/" + self.view_name_toot,
            group=True,
        )
        result_dict = {str(row.key): row.value for row in result_toots}
        # Save the dictionary to a JSON file
        if os.name == 'nt':  # Check if the operating system is Windows
            result_toots_file = f'flask_api/static/data/result_toots.json'
        else:  # Assume it's a Unix-
            result_toots_file = f'{self.workdir}/static/data/result_toots.json'
        with open(result_toots_file, "w") as jsonfile:
            json.dump(result_dict, jsonfile)
        # Print the results
        # for row in result_toots:
        #     print(row.key, row.value)





    def harvestAndPush(self, toots):
        # Fetching toots
        try:
            all_toots = toots
            document = json.dumps(all_toots)  # Convert the document to JSON string
            headers = {'Content-Type': 'application/json'}  # Specify the Content-Type header
            self.toot_db.save(json.loads(toots), headers=headers) 
            # self.toot_db.save(toots) 
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        
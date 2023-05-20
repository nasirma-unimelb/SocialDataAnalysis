import couchdb
import csv
import json
from db_gateway import Couch
import os


class Fetcher:
    def __init__(self, couchdb_master_ip, couchdb_username, couchdb_password) -> None:
        # Connect to the CouchDB server and select a database
        self.view_name_topic = "topic_Data"
        self.design_doc_name_topic = "_design/mydesign_" + self.view_name_topic

        self.view_name_target_rate = "target_rate_Data"
        self.design_doc_name_target_rate = "_design/mydesign_" + self.view_name_target_rate

        self.view_name_location = "target_location_Data"
        self.design_doc_name_location = "_design/mydesign_" + self.view_name_location

        self.view_name_inflation = "inflation_Data"
        self.design_doc_name_inflation = "_design/mydesign_" + self.view_name_inflation

        self.view_name_income_mortgage = "income_mortgage_Data"
        self.design_doc_name_income_mortgage = "_design/mydesign_" + \
            self.view_name_income_mortgage

        self.view_name_housing_total = "housing_total_Data"
        self.design_doc_name_housing_total = "_design/mydesign_" + \
            self.view_name_housing_total
        dbsl = [
            "tweet",
            "rba_target_cash_rate",
            "sudo_gccsa_income_mortgage_rent_avg_2016",
            "sudo_gccsa_housing_totals_2016",
            "sudo_gccsa_inequality_2017",
            "inflation",
        ]
        self.view_name_income_rent = "income_rent_Data"
        self.design_doc_name_income_rent = "_design/mydesign_" + self.view_name_income_rent

        self.view_name_inequality = "inequality_Data"
        self.design_doc_name_inequality = "_design/mydesign_" + self.view_name_inequality
        self.couchobj = Couch(
            f"http://{couchdb_username}:{couchdb_password}@{couchdb_master_ip}:5984/", dbsl, couchdb_username, couchdb_password)

        self.couchdbs = couchdb.Server(
            f"http://{couchdb_username}:{couchdb_password}@{couchdb_master_ip}:5984/"
        )
        self.db = self.couchdbs["tweet"]
        self.target_rate_db = self.couchdbs["rba_target_cash_rate"]
        self.inflation_db = self.couchdbs["inflation"]
        self.income_mortgage_db = self.couchdbs[
            "sudo_gccsa_income_mortgage_rent_avg_2016"
        ]
        self.housing_total_db = self.couchdbs["sudo_gccsa_housing_totals_2016"]
        self.income_rent_db = self.couchdbs["sudo_gccsa_income_mortgage_rent_avg_2016"]
        self.inequality_db = self.couchdbs["sudo_gccsa_inequality_2017"]

        self.view_name_all = "all_Data"
        self.design_doc_name_all = "_design/mydesign_/" + self.view_name_all

        self.workdir = os.getcwd()

        def get_All_Data(
            self,
        ):  # All Data View
            view_func = """function(doc) {
                    if (doc.docs) {
                        doc.docs.forEach(function(doc) {
                            emit(null, doc);
                        });
                    }
                }"""

            # Create the view if it doesn't exist

            if self.design_doc_name_all not in self.db:
                self.db[self.design_doc_name_all] = {
                    "views": {self.view_name_all: {"map": view_func}}
                }
            else:
                design_doc = self.db[self.design_doc_name_all]
                if self.view_name_all not in design_doc["views"]:
                    design_doc["views"][self.view_name_all] = {
                        "map": view_func}
                    self.db.save_doc(design_doc)

    # ----Topic View----------------------------------------------------------
    def getTweetTopicOverTime(
        self,
    ):
        view_name_topic = "topic_Data"
        design_doc_name_topic = "_design/mydesign_" + view_name_topic

        # Define the view function
        topic_func = """function (doc) {
            if (doc.docs) {
                doc.docs.forEach(function(d) {
                    var date = new Date(d.timestamp);
                    var weekStart = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay());
                    var weekNo = Math.ceil((((weekStart - new Date(weekStart.getFullYear(),0,1)) / 86400000) + 1)/7);
                    emit([d.topic, weekStart.toISOString().substring(0, 10), weekNo,d.gcc], 1);
                });
            }
        }"""

        # Define the design document name and view name
        design_doc_name = design_doc_name_topic
        view_name = view_name_topic

        # Check if the design document already exists
        if design_doc_name not in self.db:
            self.db[design_doc_name] = {
                "views": {view_name: {"map": topic_func, "reduce": "_count"}}
            }
        else:
            design_doc = self.db[design_doc_name]
            if view_name not in design_doc["views"]:
                design_doc["views"][view_name] = {
                    "map": topic_func, "reduce": "_count"}
                self.db.save(design_doc)

    # --------------------END of Topic-------------------------------------------

    # ---------Rate View------------------------------------------------------------------------
    def getTargetRateByDate(
        self,
    ):
        self.view_name_target_rate = "target_rate_Data"
        self.design_doc_name_target_rate = (
            "_design/mydesign_" + self.view_name_target_rate
        )
        # Define the view function
        target_rate_func = """function (doc) {
    if (doc.docs) {
        doc.docs.forEach(function(d) {
        var date = new Date(d.date);
        var weekStart = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay());
        var weekNo = Math.ceil((((weekStart - new Date(weekStart.getFullYear(),0,1)) / 86400000) + 1)/7);
        if (date.getDay() === 1) {
            emit(weekStart.toISOString().substring(0, 10), d.target_cash_rate);
        }
        });
    }
    }
    """

        # Define the design document name and view name
        design_doc_name = self.design_doc_name_target_rate
        view_name = self.view_name_target_rate

        # Check if the design document already exists
        if design_doc_name not in self.target_rate_db:
            self.target_rate_db[design_doc_name] = {
                "views": {view_name: {"map": target_rate_func}}
            }
        else:
            design_doc = self.target_rate_db[design_doc_name]
            if view_name not in design_doc["views"]:
                design_doc["views"][view_name] = {
                    "map": target_rate_func,
                    "reduce": "_count",
                }
                self.target_rate_db.save(design_doc)

    # -----------------------END Rate---------------------------------------------
    # --------------Location View------------------------------
    def getlocationData(
        self,
    ):
        view_name_location = "target_location_Data"
        design_doc_name_location = "_design/mydesign_" + view_name_location
        # Define the view function
        target_location_func = """function(doc) {
        if (doc.docs) {
            doc.docs.forEach(function(d) {
            var location = d.location;
            var gcc = d.gcc;
            var coordinates = d.coordinates;
            var date = new Date(d.timestamp);
            var weekStart = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay());
            if (gcc !== null && gcc !== "none" && date.getDay() === 1) {
            emit([location, gcc, coordinates, weekStart.toISOString().substring(0, 10)], 1);
            }
            });
        }
        }

        """

        # Define the design document name and view name
        design_doc_name = design_doc_name_location
        view_name = view_name_location

        # Check if the design document already exists
        if design_doc_name not in self.db:
            self.db[design_doc_name] = {
                "views": {view_name: {"map": target_location_func, "reduce": "_count"}}
            }
        else:
            design_doc = self.db[design_doc_name]
            if view_name not in design_doc["views"]:
                design_doc["views"][view_name] = {
                    "map": target_location_func,
                    "reduce": "_count",
                }
                self.target_rate_db.save(design_doc)

    # -------------End Location View -----------------

    # ---------inflation View------------------------------------------------------------------------
    def getinflationByDate(
        self,
    ):
        self.view_name_inflation = "inflation_Data"
        self.design_doc_name_inflation = "_design/mydesign_" + self.view_name_inflation
        # Define the view function
        inflation_func = """function (doc) {
    if (doc.docs) {
        doc.docs.forEach(function(d) {
        var date = new Date(d.date);
        var weekStart = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay());
        var weekNo = Math.ceil((((weekStart - new Date(weekStart.getFullYear(),0,1)) / 86400000) + 1)/7);
        if (date.getDay() === 1) {
            emit(date.toISOString().substring(0, 10), d.cpi);
        }
        });
    }
    }
    """

        # Define the design document name and view name
        design_doc_name = self.design_doc_name_inflation
        view_name = self.view_name_inflation

        # Check if the design document already exists
        if design_doc_name not in self.inflation_db:
            self.inflation_db[design_doc_name] = {
                "views": {view_name: {"map": inflation_func}}
            }
        else:
            design_doc = self.inflation_db[design_doc_name]
            if view_name not in design_doc["views"]:
                design_doc["views"][view_name] = {
                    "map": inflation_func,
                    "reduce": "_count",
                }
                self.inflation_db.save(design_doc)

    # -----------------------END inflation---------------------------------------------

    # ---------income_mortgage View------------------------------------------------------------------------
    def get_income_mortgage(
        self,
    ):
        view_name_income_mortgage = "income_mortgage_Data"
        design_doc_name_income_mortgage = (
            "_design/mydesign_" + view_name_income_mortgage
        )
        # Define the view function
        income_mortgage_func = """function (doc) {
    if (doc.docs) {
        doc.docs.forEach(function(d) {
            emit(d.gcc_code16, d.median_mortgage_repay_monthly);
        });
    }
    }

    """

        # Define the design document name and view name
        design_doc_name = design_doc_name_income_mortgage
        view_name = view_name_income_mortgage

        # Check if the design document already exists
        if design_doc_name not in self.income_mortgage_db:
            self.income_mortgage_db[design_doc_name] = {
                "views": {view_name: {"map": income_mortgage_func}}
            }
        else:
            design_doc = self.income_mortgage_db[design_doc_name]
            if view_name not in design_doc["views"]:
                design_doc["views"][view_name] = {
                    "map": income_mortgage_func,
                    "reduce": "_count",
                }
                self.income_mortgage_db.save(design_doc)

    # -----------------------END income_mortgage---------------------------------------------

    # ---------housing_total View------------------------------------------------------------------------
    def get_housing_total(
        self,
    ):
        self.view_name_housing_total = "housing_total_Data"
        self.design_doc_name_housing_total = (
            "_design/mydesign_" + self.view_name_housing_total
        )
        # Define the view function
        housing_total_func = """
    function (doc) {
    if (doc.docs) {
        doc.docs.forEach(function(d) {
            var value = {
                own_outright_total: d.own_outright_total,
                own_mortgage_total: d.own_mortgage_total,
                rent_total: d.rent_total
            };
            emit(d.gcc_code16, value);
        });
    }
    }
    """

        # Define the design document name and view name
        design_doc_name = self.design_doc_name_housing_total
        view_name = self.view_name_housing_total

        # Check if the design document already exists
        if design_doc_name not in self.housing_total_db:
            self.housing_total_db[design_doc_name] = {
                "views": {view_name: {"map": housing_total_func}}
            }
        else:
            design_doc = self.housing_total_db[design_doc_name]
            if view_name not in design_doc["views"]:
                design_doc["views"][view_name] = {
                    "map": housing_total_func,
                    "reduce": "_count",
                }
                self.housing_total_db.save(design_doc)

    # -----------------------END housing_total---------------------------------------------

    # ---------income_rent View------------------------------------------------------------------------
    def get_income_rent(
        self,
    ):
        self.view_name_income_rent = "income_rent_Data"
        self.design_doc_name_income_rent = (
            "_design/mydesign_" + self.view_name_income_rent
        )
        # Define the view function
        income_rent_func = """
    function (doc) {
    if (doc.docs) {
        doc.docs.forEach(function(d) {
            var value = {
                median_tot_hhd_inc_weekly: d.median_tot_hhd_inc_weekly,
                median_mortgage_repay_monthly: d.median_mortgage_repay_monthly
            };
            emit(d.gcc_code16, value);
        });
    }
    }

    """

        # Define the design document name and view name
        design_doc_name = self.design_doc_name_income_rent
        view_name = self.view_name_income_rent

        # Check if the design document already exists
        if design_doc_name not in self.income_rent_db:
            self.income_rent_db[design_doc_name] = {
                "views": {view_name: {"map": income_rent_func}}
            }
        else:
            design_doc = self.income_rent_db[design_doc_name]
            if view_name not in design_doc["views"]:
                design_doc["views"][view_name] = {
                    "map": income_rent_func,
                    "reduce": "_count",
                }
                self.income_rent_db.save(design_doc)

    # -----------------------END income_rent---------------------------------------------

    # ---------inequality View------------------------------------------------------------------------
    def get_inequality(
        self,
    ):
        self.view_name_inequality = "inequality_Data"
        self.design_doc_name_inequality = (
            "_design/mydesign_" + self.view_name_inequality
        )
        # Define the view function
        inequality_func = """function (doc) {
    if (doc.docs) {
        doc.docs.forEach(function(d) {
            var value = {
                earners_persons: d.earners_persons,
                median_age_of_earners_years: d.median_age_of_earners_years,
                gini_coefficient_coef: d.gini_coefficient_coef
            };
            emit(d.gccsa_code, value);
        });
    }
    }
    """

        # Define the design document name and view name
        design_doc_name = self.design_doc_name_inequality
        view_name = self.view_name_inequality

        # Check if the design document already exists
        if design_doc_name not in self.inequality_db:
            self.inequality_db[design_doc_name] = {
                "views": {view_name: {"map": inequality_func}}
            }
        else:
            design_doc = self.inequality_db[design_doc_name]
            if view_name not in design_doc["views"]:
                design_doc["views"][view_name] = {
                    "map": inequality_func,
                    "reduce": "_count",
                }
                self.inequality_db.save(design_doc)

    # -----------------------END inequality---------------------------------------------

    def save_target_rates(
        self,
    ):
        # Query the view
        self.getTargetRateByDate()
        result_target_rates = self.target_rate_db.view(
            self.design_doc_name_target_rate + "/_view/" + self.view_name_target_rate,
            group=False,
        )
        result_dict = {row.key: row.value for row in result_target_rates}

        # Save the dictionary to a JSON file
        result_target_rates_file = f'{self.workdir}/static/data/result_target_rates.json'
        with open(result_target_rates_file, "w") as jsonfile:
            json.dump(result_dict, jsonfile)
        # Print the results
        for row in result_target_rates:
            print(row.key, row.value)

        # with open('../flask_api/static/data/result_topics.csv', 'w', newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(['value'])
        #     for row in result_topics:
        #         writer.writerow([row.value])

    def save_inflations(
        self,
    ):
        # Query the view
        self.getinflationByDate()
        result_inflations = self.inflation_db.view(
            self.design_doc_name_inflation + "/_view/" + self.view_name_inflation,
            group=False,
        )
        result_dict = {row.key: row.value for row in result_inflations}

        # Save the dictionary to a JSON file
        result_inflations_file = f'{self.workdir}/static/data/result_inflations.json'
        with open(result_inflations_file, "w") as jsonfile:
            json.dump(result_dict, jsonfile)
        # Print the results
        for row in result_inflations:
            print(row.key, row.value)

        # with open('../flask_api/static/data/result_topics.csv', 'w', newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(['value'])
        #     for row in result_topics:
        #         writer.writerow([row.value])

    def save_housing_totals(
        self,
    ):
        # Query the view
        self.get_housing_total()
        result_housing_totals = self.housing_total_db.view(
            self.design_doc_name_housing_total
            + "/_view/"
            + self.view_name_housing_total,
            group=False,
        )
        result_dict = {row.key: row.value for row in result_housing_totals}

        # Save the dictionary to a JSON file
        result_housing_totals_file = f'{self.workdir}/static/data/result_inflations.json'
        with open(result_housing_totals_file, "w") as jsonfile:
            json.dump(result_dict, jsonfile)
        # Print the results
        for row in result_housing_totals:
            print(row.key, row.value)

        # with open('../flask_api/static/data/result_topics.csv', 'w', newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(['value'])
        #     for row in result_topics:
        #         writer.writerow([row.value])

    def save_inequality(
        self,
    ):
        # Query the view
        self.get_inequality()
        result_inequalitys = self.inequality_db.view(
            self.design_doc_name_inequality + "/_view/" + self.view_name_inequality,
            group=False,
        )
        result_dict = {row.key: row.value for row in result_inequalitys}

        # Save the dictionary to a JSON file
        result_inequalitys_file = f'{self.workdir}/static/data/result_inequalitys.json'
        with open(result_inequalitys_file, "w") as jsonfile:
            json.dump(result_dict, jsonfile)
        # Print the results
        for row in result_inequalitys:
            print(row.key, row.value)

        # with open('../flask_api/static/data/result_topics.csv', 'w', newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(['value'])
        #     for row in result_topics:
        #         writer.writerow([row.value])

    def save_income_rents(
        self,
    ):
        # Query the view
        self.get_income_rent()
        result_income_rents = self.income_rent_db.view(
            self.design_doc_name_income_rent + "/_view/" + self.view_name_income_rent,
            group=False,
        )
        result_dict = {row.key: row.value for row in result_income_rents}

        # Save the dictionary to a JSON file
        result_income_rents_file = f'{self.workdir}/static/data/result_income_rents.json'
        with open(result_income_rents_file, "w") as jsonfile:
            json.dump(result_dict, jsonfile)
        # Print the results
        for row in result_income_rents:
            print(row.key, row.value)

        # with open('../flask_api/static/data/result_topics.csv', 'w', newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(['value'])
        #     for row in result_topics:
        #         writer.writerow([row.value])

    def save_income_mortgages(
        self,
    ):
        # Query the view
        self.get_income_mortgage()
        result_income_mortgages = self.income_mortgage_db.view(
            self.design_doc_name_income_mortgage
            + "/_view/"
            + self.view_name_income_mortgage,
            group=False,
        )
        result_dict = {row.key: row.value for row in result_income_mortgages}

        # Save the dictionary to a JSON file
        result_income_mortgages_file = f'{self.workdir}/static/data/result_income_mortgages.json'
        with open(
            result_income_mortgages_file, "w"
        ) as jsonfile:
            json.dump(result_dict, jsonfile)
        # Print the results
        for row in result_income_mortgages:
            print(row.key, row.value)

        # with open('../flask_api/static/data/result_topics.csv', 'w', newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(['value'])
        #     for row in result_topics:
        #         writer.writerow([row.value])

    def save_all(
        self,
    ):
        # Query the view
        result_all = self.db.view(
            self.design_doc_name_all + "/_view/" + self.view_name_all
        )

        # Print the first 5 rows of the results
        for i, row in enumerate(result_all):
            if i < 5:
                print(row.value)
            else:
                break
        # with open('../flask_api/static/data/results_all.csv', 'w', newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(['value'])
        #     for row in result_all:
        #         writer.writerow([row.value])

        # Save the results to a JSON file
        with open("../flask_api/static/data/results_all.json", "w") as jsonfile:
            json.dump([row.value for row in result_all], jsonfile)
        # Print the results
        # for row in result_all:
        #     print(row.value)

    # Query the view
    def save_Topic_over_time(
        self,
    ):
        self.getTweetTopicOverTime()
        result_topics = self.db.view(
            self.design_doc_name_topic + "/_view/" + self.view_name_topic, group=True
        )
        result_dict = {str(row.key): row.value for row in result_topics}
        # Save the dictionary to a JSON file
        result_topics_file = f'{self.workdir}/static/data/result_topics.json'
        with open(result_topics_file, "w") as jsonfile:
            json.dump(result_dict, jsonfile)
        # Print the results
        # for row in result_topics:
        #     print(row.key, row.value)

    def save_Location_data(
        self,
    ):
        self.getlocationData()
        result_locations = self.db.view(
            self.design_doc_name_location + "/_view/" + self.view_name_location,
            group=True,
        )
        result_dict = {str(row.key): row.value for row in result_locations}
        # Save the dictionary to a JSON file
        result_locations_file = f'{self.workdir}/static/data/result_locations.json'
        with open(result_locations_file, "w") as jsonfile:
            json.dump(result_dict, jsonfile)
        # Print the results
        # for row in result_locations:
        #     print(row.key, row.value)

    def get_rural_urban(self, gcc):
        if gcc.startswith("1"):
            return "metropolitan"
        else:
            return "rural"

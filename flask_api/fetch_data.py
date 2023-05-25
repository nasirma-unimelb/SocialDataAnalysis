import couchdb
import json
from db_gateway import Couch
import os


class Fetcher:
    def __init__(self, couchdb_master_ip, couchdb_username, couchdb_password) -> None:
        # Connect to the CouchDB server and select a database
        self.view_name_topic = "topic_Data"
        self.design_doc_name_topic = "_design/mydesign_" + self.view_name_topic

        self.view_name_target_rate = "target_rate_Data"
        self.design_doc_name_target_rate = (
            "_design/mydesign_" + self.view_name_target_rate
        )

        self.view_name_location = "target_location_Data"
        self.design_doc_name_location = "_design/mydesign_" + self.view_name_location

        self.view_name_inflation = "inflation_Data"
        self.design_doc_name_inflation = "_design/mydesign_" + self.view_name_inflation

        self.view_name_income_mortgage = "income_mortgage_Data"
        self.design_doc_name_income_mortgage = (
            "_design/mydesign_" + self.view_name_income_mortgage
        )

        self.view_name_housing_total = "housing_total_Data"
        self.design_doc_name_housing_total = (
            "_design/mydesign_" + self.view_name_housing_total
        )
        dbsl = [
            "tweet",
            "rba_target_cash_rate",
            "sudo_gccsa_income_mortgage_rent_avg_2016",
            "sudo_gccsa_housing_totals_2016",
            "sudo_gccsa_inequality_2017",
            "inflation",
        ]
        self.view_name_income_rent = "income_rent_Data"
        self.design_doc_name_income_rent = (
            "_design/mydesign_" + self.view_name_income_rent
        )

        self.view_name_inequality = "inequality_Data"
        self.design_doc_name_inequality = (
            "_design/mydesign_" + self.view_name_inequality
        )

        self.view_name_toot = "toot_Data"
        self.design_doc_name_toot = "_design/mydesign_" + self.view_name_toot

        self.couchobj = Couch(
            f"http://{couchdb_username}:{couchdb_password}@{couchdb_master_ip}:5984/",
            dbsl,
            couchdb_username,
            couchdb_password,
            False,
        )

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
        self.toot_db = self.couchdbs["toot"]

        self.workdir = os.getcwd()

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
            var topic = d.topic;
            var gcc = d.gcc;
            var week = d.week;
            var date = new Date(d.timestamp);
            var weekStart = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay());
               if (gcc !== null && gcc !== "none" && date.getDay() === 1) {
            emit([topic, gcc, week], 1);
               }
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
                design_doc["views"][view_name] = {"map": topic_func, "reduce": "_count"}
                self.db.save(design_doc)
        # Define the index function
        index_func = {
            "index": {"fields": ["docs.topic", "docs.timestamp", "docs.gcc"]},
            "name": "topic-time-gcc-index",
            "type": "json",
        }

        # Check if the design document already exists
        if design_doc_name_topic not in self.db:
            self.db[design_doc_name_topic] = {"indexes": [index_func]}
        else:
            design_doc = self.db[design_doc_name_topic]
            if "indexes" not in design_doc:
                design_doc["indexes"] = [index_func]
            else:
                design_doc["indexes"].append(index_func)
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
    for (var i = 0; i < doc.docs.length; i++) {
      var data = doc.docs[i];
      if (data.date && data.target_cash_rate) {
        emit(data.date, data.target_cash_rate);
      }
    }
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
    for (var i = 0; i < doc.docs.length; i++) {
      var data = doc.docs[i];
      if (data.date && data.cpi) {
        emit(data.date, data.cpi);
      }
    }
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

    # ---------toot View------------------------------------------------------------------------
    def get_toot(
        self,
    ):
        self.view_name_toot = "toot_Data"
        self.design_doc_name_toot = "_design/mydesign_" + self.view_name_toot
        # Define the view function
        toot_func = """function(doc) {
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
        toot_reduce_func = """function(keys, values, rereduce) {
  return sum(values);
}
"""

        # Define the design document name and view name
        design_doc_name = self.design_doc_name_toot
        view_name = self.view_name_toot

        # Check if the design document already exists
        if design_doc_name not in self.toot_db:
            self.toot_db[design_doc_name] = {"views": {view_name: {"map": toot_func}}}
        else:
            design_doc = self.toot_db[design_doc_name]
            if view_name not in design_doc["views"]:
                design_doc["views"][view_name] = {
                    "map": toot_func,
                    "reduce": toot_reduce_func,
                }
                self.toot_db.save(design_doc)

    # -----------------------END toot---------------------------------------------

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
        if os.name == "nt":  # Check if the operating system is Windows
            result_target_rates_file = f"flask_api/static/data/result_target_rates.json"
        else:  # Assume it's a Unix-
            result_target_rates_file = (
                f"{self.workdir}/static/data/result_target_rates.json"
            )

        with open(result_target_rates_file, "w") as jsonfile:
            json.dump(result_dict, jsonfile)

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
        if os.name == "nt":  # Check if the operating system is Windows
            result_inflations_file = f"flask_api/static/data/result_inflations.json"
        else:  # Assume it's a Unix-
            result_inflations_file = (
                f"{self.workdir}/static/data/result_inflations.json"
            )

        with open(result_inflations_file, "w") as jsonfile:
            json.dump(result_dict, jsonfile)

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
        if os.name == "nt":  # Check if the operating system is Windows
            result_housing_totals_file = f"flask_api/static/data/housing_totals.json"
        else:  # Assume it's a Unix-
            result_housing_totals_file = (
                f"{self.workdir}/static/data/housing_totals.json"
            )
        with open(result_housing_totals_file, "w") as jsonfile:
            json.dump(result_dict, jsonfile)
        # Print the results

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
        if os.name == "nt":  # Check if the operating system is Windows
            result_inequalitys_file = f"flask_api/static/data/result_inequalitys.json"
        else:  # Assume it's a Unix-
            result_inequalitys_file = (
                f"{self.workdir}/static/data/result_inequalitys.json"
            )

        with open(result_inequalitys_file, "w") as jsonfile:
            json.dump(result_dict, jsonfile)
        # Print the results

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
        if os.name == "nt":  # Check if the operating system is Windows
            result_income_rents_file = f"flask_api/static/data/result_income_rents.json"
        else:  # Assume it's a Unix-
            result_income_rents_file = (
                f"{self.workdir}/static/data/result_income_rents.json"
            )

        with open(result_income_rents_file, "w") as jsonfile:
            json.dump(result_dict, jsonfile)
        # Print the results

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
        if os.name == "nt":  # Check if the operating system is Windows
            result_income_mortgages_file = (
                f"flask_api/static/data/result_income_mortgages.json"
            )
        else:  # Assume it's a Unix-
            result_income_mortgages_file = (
                f"{self.workdir}/static/data/result_income_mortgages.json"
            )

        with open(result_income_mortgages_file, "w") as jsonfile:
            json.dump(result_dict, jsonfile)
        # Print the results

        # with open('../flask_api/static/data/result_topics.csv', 'w', newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(['value'])
        #     for row in result_topics:
        #         writer.writerow([row.value])

    # Query the view

    def save_Topic_over_time(
        self,
    ):
        self.getTweetTopicOverTime()
        result_topics = self.db.view(
            self.design_doc_name_topic + "/_view/" + self.view_name_topic,
            group=True,
            stale="ok",
        )
        result_dict = {str(row.key): row.value for row in result_topics}
        # Save the dictionary to a JSON file
        if os.name == "nt":  # Check if the operating system is Windows
            result_topics_file = f"flask_api/static/data/result_topics.json"
        else:  # Assume it's a Unix-
            result_topics_file = f"{self.workdir}/static/data/result_topics.json"

        with open(result_topics_file, "w") as jsonfile:
            json.dump(result_dict, jsonfile)

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
        if os.name == "nt":  # Check if the operating system is Windows
            result_locations_file = f"flask_api/static/data/result_locations.json"
        else:  # Assume it's a Unix-
            result_locations_file = f"{self.workdir}/static/data/result_locations.json"
        with open(result_locations_file, "w") as jsonfile:
            json.dump(result_dict, jsonfile)
        # Print the results
        # for row in result_locations:
        #     print(row.key, row.value)

    def get_rural_urban(self, gcc):
        if gcc[1] == "r":
            return "rural"
        else:
            return "metropolitan"

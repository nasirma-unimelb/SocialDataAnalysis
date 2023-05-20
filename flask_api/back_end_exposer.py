# from fetch_data import (
#     save_target_rates,
#     save_Topic_over_time,
#     save_Location_data,
#     save_inflations,
#     save_income_mortgages,
#     save_housing_totals,
#     save_inequality,
#     get_rural_urban,
# )

from fetch_data import Fetcher
from flask import Flask, render_template, send_file, request, url_for, redirect
from collections import defaultdict
import json
import pandas as pd
import argparse
import os
from flask_cors import CORS


def pre_task(fetcher: Fetcher):
    workdir = os.getcwd()

    # Load the JSON
    results_topics_file = f'{workdir}/static/data/result_topics.json'
    fetcher.save_Topic_over_time()
    with open(results_topics_file) as f:
        data = json.load(f)

    # Convert the JSON data into a DataFrame
    df_locs = pd.DataFrame.from_dict(data, orient="index", columns=["value"])

    df_locs.reset_index(inplace=True)
    df_locs[["type", "date", "week_number", "gcc"]] = pd.DataFrame(
        df_locs["index"].apply(eval).tolist()
    )

    df_locs.drop("index", axis=1, inplace=True)

    # ---Rate Data-----------------------
    result_target_rates_file = f'{workdir}/static/data/result_target_rates.json'
    fetcher.save_target_rates()
    with open(result_target_rates_file) as f:
        rate_data = json.load(f)
    # Print the resulting DataFrame

    # df_rate = [{'date': date, 'target_cash_rate': rate} for date, rate in rate_data.items()]

    df_rate = pd.DataFrame.from_dict(
        rate_data, orient="index", columns=["target_cash_rate"]
    )
    df_rate.index.name = "date"
    df_rate.reset_index(inplace=True)
    df_rate["date"] = pd.to_datetime(df_rate["date"])
    df_locs["date"] = pd.to_datetime(df_locs["date"])

    # convert the date column to datetime type

    # join the two DataFrames on the date column
    df_tweet_rate = pd.merge(df_locs, df_rate, on="date")

    # ----------End Rate--------------------------------------
    # ---Location Data---------------------------------------
    def get_location():
        result_locations_file = f'{workdir}/static/data/result_locations.json'
        fetcher.save_Location_data()
        with open(result_locations_file) as f:
            location_data = json.load(f)
        df_location = pd.DataFrame(
            [
                [eval(key)[0], eval(key)[1], eval(key)[2], eval(key)[3], value]
                for key, value in location_data.items()
            ],
            columns=["Location", "gcc", "Coordinates", "date", "Count"],
        )

        df_location["date"] = pd.to_datetime(df_location["date"])
        return df_location

    # ----End Location------------------------

    # ---inflation Data-----------------------
    result_inflations_file = f'{workdir}/static/data/result_inflations.json'
    fetcher.save_inflations()
    with open(result_inflations_file) as f:
        inflation_data = json.load(f)
    # Print the resulting DataFrame

    # df_inflation = [{'date': date, 'target_cash_inflation': inflation} for date, inflation in inflation_data.items()]

    df_inflation = pd.DataFrame.from_dict(
        inflation_data, orient="index", columns=["cpi"]
    )
    df_inflation.index.name = "date"
    df_inflation.reset_index(inplace=True)
    df_inflation["date"] = pd.to_datetime(df_inflation["date"])

    # convert the date column to datetime type
    # Make a copy of the DataFrame
    df_inflation_copy = df_locs.copy()

    # Convert the 'date' column to datetime type
    df_inflation_copy["date"] = pd.to_datetime(df_inflation_copy["date"])

    # Modify the 'date' column to the first day of each month
    # Rename the 'week_number' column to 'weekno'
    # df_inflation_copy = df_inflation_copy.rename(columns={'week_number': 'weekno'})

    df_inflation_copy["weekno"] = df_inflation_copy["date"].dt.isocalendar().week

    df_inflation["weekno"] = df_inflation["date"].dt.isocalendar().week

    # Join the two DataFrames on the modified 'date' column
    df_tweet_inflation = pd.merge(
        df_inflation_copy[df_inflation_copy["type"] == "inflation"],
        df_inflation,
        on="weekno",
    )

    # ----------End inflation--------------------------------------

    # ---income_mortgage Data-----------------------
    result_income_mortgages_file = f'{workdir}/static/data/result_income_mortgages.json'
    fetcher.save_income_mortgages()
    with open(result_income_mortgages_file) as f:
        income_mortgage_data = json.load(f)
    # Print the resulting DataFrame

    # df_income_mortgage = [{'date': date, 'target_cash_income_mortgage': income_mortgage} for date, income_mortgage in income_mortgage_data.items()]

    df_income_mortgage = pd.DataFrame.from_dict(
        income_mortgage_data, orient="index", columns=["median_mortgage_repay_monthly"]
    )
    df_income_mortgage.index.name = "gcc_code16"
    df_income_mortgage.reset_index(inplace=True)

    df_income_mortgage = df_income_mortgage.rename(
        columns={"gcc_code16": "gcc"})
    df_income_mortgage["gcc"] = df_income_mortgage["gcc"].str.lower()

    # convert the date column to datetime type
    # Make a copy of the DataFrame
    df_loc = get_location()
    df_grouped = df_loc.groupby("gcc")["Count"].sum().reset_index()

    # Convert the 'date' column to datetime type

    # Modify the 'date' column to the first day of each month
    # Rename the 'week_number' column to 'weekno'

    # df_income_mortgage_copy['weekno'] = df_income_mortgage_copy['date'].dt.isocalendar().week

    # df_income_mortgage['weekno'] = df_income_mortgage['date'].dt.isocalendar().week

    # Join the two DataFrames on the modified 'date' column
    df_tweet_income_mortgage = pd.merge(
        df_grouped, df_income_mortgage, on="gcc")

    # ----------End income_mortgage--------------------------------------

    # ---housing_total Data-----------------------
    result_housing_totals_file = f'{workdir}/static/data/result_housing_totals.json'
    fetcher.save_housing_totals()
    with open(result_housing_totals_file) as f:
        housing_total_data = json.load(f)
    # Print the resulting DataFrame

    # df_housing_total = [{'date': date, 'target_cash_housing_total': housing_total} for date, housing_total in housing_total_data.items()]

    df_housing_total = pd.DataFrame.from_dict(
        housing_total_data,
        orient="index",
        columns=["own_outright_total", "own_mortgage_total", "rent_total"],
    )
    df_housing_total.index.name = "gcc_code16"
    df_housing_total.reset_index(inplace=True)

    df_housing_total = df_housing_total.rename(columns={"gcc_code16": "gcc"})
    df_housing_total["gcc"] = df_housing_total["gcc"].str.lower()

    # Join the two DataFrames on the modified 'date' column
    df_tweet_housing_total = pd.merge(df_grouped, df_housing_total, on="gcc")

    # ----------End housing_total--------------------------------------

    # ---inequality Data-----------------------
    result_inequalitys_file = f'{workdir}/static/data/result_inequalitys.json'
    fetcher.save_inequality()
    with open(result_inequalitys_file) as f:
        inequality_data = json.load(f)
    # Print the resulting DataFrame

    # df_inequality = [{'date': date, 'target_cash_inequality': inequality} for date, inequality in inequality_data.items()]

    df_inequality = pd.DataFrame.from_dict(
        inequality_data,
        orient="index",
        columns=[
            "earners_persons",
            "median_age_of_earners_years",
            "gini_coefficient_coef",
        ],
    )
    df_inequality.index.name = "gccsa_code"
    df_inequality.reset_index(inplace=True)

    df_inequality = df_inequality.rename(columns={"gccsa_code": "gcc"})
    df_inequality["gcc"] = df_inequality["gcc"].str.lower()
    df_loc_tweets = df_locs.groupby(["type"])["value"].sum().reset_index()

    grouped_df = df_locs.groupby(["gcc", "type"])["value"].sum().reset_index()

    # Pivot the data to get the desired format
    pivot_df = pd.pivot_table(
        grouped_df, index="gcc", columns="type", values="value", aggfunc="sum"
    )

    # Convert the pivot table to a dictionary in the desired format
    tweetsByTopicGrouped_arr = []
    for index, row in pivot_df.iterrows():
        data_row = {
            "gcc": index,
            "housing": int(row["housing"]) if not pd.isna(row["housing"]) else 0,
            "inflation": int(row["inflation"]) if not pd.isna(row["inflation"]) else 0,
            "interestRate": int(row["interest rate"])
            if not pd.isna(row["interest rate"])
            else 0,
            "socialSecurity": int(row["social security"])
            if not pd.isna(row["social security"])
            else 0,
        }
        tweetsByTopicGrouped_arr.append(data_row)
    df_tweetsByTopicGrouped = pd.DataFrame(tweetsByTopicGrouped_arr)
    combined_df = pd.merge(df_tweetsByTopicGrouped, df_housing_total, on="gcc")
    combined_df = pd.merge(combined_df, df_inequality, on="gcc")
    combined_df = pd.merge(combined_df, df_income_mortgage, on="gcc")
    for col in combined_df.columns:
        if col in ["housing", "inflation", "interestRate", "socialSecurity"]:
            combined_df[f"{col}_pc"] = (
                combined_df[col] / combined_df.earners_persons * 100_000
            )
    for col in combined_df.columns:
        if col in ["rent_total", "own_mortgage_total", "own_outright_total"]:
            combined_df[f"{col}_pc"] = combined_df[col] / \
                combined_df.earners_persons
    combined_df["rural_urban"] = combined_df["gcc"].apply(
        lambda gcc: fetcher.get_rural_urban(gcc)
    )
    # combined_df= combined_df.rename(columns={'U': 'metropolitan'})
    # combined_df= combined_df.rename(columns={'R': 'rural'})
    # ----------End inequality--------------------------------------

    app = Flask(__name__)

    @app.route("/refresh", methods=["GET", "POST"])
    def refresh_stats():
        fetcher.save_Topic_over_time()
        fetcher.save_target_rates()
        fetcher.save_Location_data()
        # save_all
        return render_template("index.html")

    @app.route("/tweetsByTopic")
    def tweetsByTopic():
        df_locs["date"] = pd.to_datetime(df_locs["date"])
        df_locs["date"] = df_locs["date"].dt.strftime("%Y-%m-%d")
        data = {
            "meta": {
                "xLabel": "Week",
                "YLabel": "Interest Rate",
                "barLabels": list(df_locs.columns),
            },
            "data": df_locs.reset_index().to_dict(orient="records"),
        }
        return data

    @app.route("/tweetsByTopicGrouped")
    def tweetsByTopicGroupedFunc():
        # Create the final dictionary structure
        final_data = {
            "meta": {
                "xLabel": "Week",
                "yLabel": "Tweets",
                "barLabels": ["housing", "inflation", "interestRate", "socialSecurity"],
            },
            "data": tweetsByTopicGrouped_arr,
        }

        # Serialize the final_data dictionary to JSON
        json_data = json.dumps(final_data)
        return json_data

    @app.route("/targtRateByTweets")
    def targtRateByTweets():
        if df_tweet_rate["date"].notnull().all():
            df_tweet_rate["date"] = pd.to_datetime(df_locs["date"])
            df_tweet_rate["date"] = df_tweet_rate["date"].dt.strftime(
                "%Y-%m-%d")
        data = {
            "meta": {
                "xLabel": "Week",
                "leftYLabel": "RBA Rate",
                "rightYLabel": "Tweets",
            },
            "data": [
                {"Week": week_no, "RBA Rate": target_rate, "Tweets": value}
                for week_no, target_rate, value in zip(
                    df_tweet_rate["week_number"],
                    df_tweet_rate["target_cash_rate"],
                    df_tweet_rate["value"],
                )
            ],
        }
        json_data = json.dumps(data)
        return json_data

    @app.route("/inflationTweetsByDate")
    def inflationTweetsByDate():
        data = {
            "meta": {
                "xLabel": "Week",
                "leftYLabel": "Inflation",
                "rightYLabel": "Tweets",
            },
            "data": [
                {"Week": int(week_no), "Inflation": cpi,
                 "Tweets": float(value)}
                for week_no, cpi, value in zip(
                    df_tweet_inflation["weekno"],
                    df_tweet_inflation["cpi"],
                    df_tweet_inflation["value"],
                )
            ],
        }

        if not data["data"]:
            return {}  # Return an empty JSON object if data is empty

        json_data = json.dumps(data)
        return json_data

    @app.route("/income_mortgage_Tweets")
    def income_mortgage_Tweets():
        data = {
            "meta": {
                "xLabel": "gcc",
                "leftYLabel": "income_mortgage",
                "rightYLabel": "Tweet Count",
            },
            "data": [
                {
                    "xAxis": gcc,
                    "leftYAxis": median_mortgage_repay_monthly,
                    "rightYAxis": count,
                }
                for gcc, median_mortgage_repay_monthly, count in zip(
                    df_tweet_income_mortgage["gcc"],
                    df_tweet_income_mortgage["median_mortgage_repay_monthly"],
                    df_tweet_income_mortgage["Count"],
                )
            ],
        }
        json_data = json.dumps(data)
        return json_data

    @app.route("/larger_mortgage_with_interestRate")
    def larger_mortgage_with_interestRate():
        grouped_df_ru = combined_df.groupby("rural_urban")

        # Define the meta information
        meta = {
            "xLabel": "Mortgage",
            "yLabel": "Interest Rate",
            "zLabel": "gcc",
            "categories": ["metropolitan", "rural"],
        }

        # Initialize the data dictionary
        data = {"meta": meta, "metropolitan": [], "rural": []}

        # Define a function to construct the data points for each group
        def construct_data_points(group_name, grouped_df_ru):
            data_points = []
            for index, row in grouped_df_ru.iterrows():
                data_point = {
                    "gcc": row["gcc"],
                    "Mortgage": row["median_mortgage_repay_monthly"],
                    "Interest Rate": row["interestRate_pc"],
                }
                data_points.append(data_point)
            data[group_name] = data_points

        # Apply the function to each group
        grouped_df_ru.apply(lambda x: construct_data_points(x.name, x))
        data = json.dumps(data)
        return data

    @app.route("/own_outright_vs_mortgage")
    def own_outright_vs_mortgage():
        grouped_df_ru = combined_df.groupby("rural_urban")

        # Define the meta information
        meta = {
            "xLabel": "Ownership",
            "yLabel": "Interest Rate",
            "zLabel": "gcc",
            "categories": ["metropolitan", "rural"],
        }

        # Initialize the data dictionary
        data = {"meta": meta, "metropolitan": [], "rural": []}

        # Define a function to construct the data points for each group
        def construct_data_points(group_name, grouped_df_ru):
            data_points = []
            for index, row in grouped_df_ru.iterrows():
                data_point = {
                    "gcc": row["gcc"],
                    "Ownership": row["own_outright_total_pc"],
                    "Interest Rate": row["interestRate_pc"],
                }
                data_points.append(data_point)
            data[group_name] = data_points

        # Apply the function to each group
        grouped_df_ru.apply(lambda x: construct_data_points(x.name, x))
        data = json.dumps(data)
        return data

    @app.route("/targtRateByDate")
    def targtRateByDate():
        if df_rate["date"].notnull().all():
            df_rate["date"] = pd.to_datetime(df_locs["date"])
            df_rate["date"] = df_rate["date"].dt.strftime("%Y-%m-%d")
        return df_rate.to_json(orient="records")

    @app.route("/locationByDate")
    def locationByDate():
        df_location = get_location()
        if df_location["date"].notnull().all():
            df_location["date"] = pd.to_datetime(df_location["date"]).dt.strftime(
                "%Y-%m-%d"
            )
        return df_location.to_json(orient="records")

    @app.route("/locationTweetCounts")
    def locationTweetCounts():
        df_location = get_location()
        grouped_data = {}

        for index, row in df_location.iterrows():
            gcc = row["gcc"]
            count = row["Count"]

            if gcc not in grouped_data:
                grouped_data[gcc] = 0

            grouped_data[gcc] += count

        result = [{"gcc": gcc, "tweets": count}
                  for gcc, count in grouped_data.items()]
        return result

    return app


if __name__ == "__main__":
    FE_DDOMAIN_DEV = "http://localhost:3000"

    parser = argparse.ArgumentParser(
        description="Expose the backend"
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

    args = parser.parse_args()

    fetcher = Fetcher(
        args.couchdb_master_ip, args.couchdb_username, args.couchdb_password
    )

    app = pre_task(fetcher=fetcher)
    cors = CORS(app, resources={r"/*": {"origins": FE_DDOMAIN_DEV}})
    app.run(debug=True, use_reloader=True)

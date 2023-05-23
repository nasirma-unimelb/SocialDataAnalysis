from fetch_data import Fetcher
from flask import Flask, jsonify, render_template, send_file, request, url_for, redirect
import json
import pandas as pd
import argparse
import os
from flask_cors import CORS
import sys
from harvester import FetcherHarverster
import datetime as dt
import numpy as np

parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(parent_dir, "..", "HarvestorAndDBLoader"))


def pre_task(fetcher: Fetcher):
    workdir = os.getcwd()
    # ---toot Data---------------------------------------

    # Load the JSON
    if os.name == "nt":  # Check if the operating system is Windows
        results_topics_file = f"{workdir}/flask_api/static/data/result_topics.json"
        twitter_file = f"{workdir}/flask_api/data/twitter/twitter.json"
    else:  # Assume it's a Unix-
        results_topics_file = f"{workdir}/static/data/result_topics.json"
        twitter_file = os.path.join(f"{workdir}", "data", "twitter", "twitter.json")

    fetcher.save_Topic_over_time()
    try:
        with open(twitter_file) as f:
            data = json.load(f)
        df_locs = pd.DataFrame.from_dict(data["docs"])
        df_tweets = pd.DataFrame.from_dict(data["docs"])
    except:
        pass
    try:
        with open(results_topics_file) as f:
            data = json.load(f)

            # Convert the JSON data into a DataFrame
            if len(data) > 0:
                df_locs = pd.DataFrame.from_dict(
                    data, orient="index", columns=["value"]
                )
                df_tweets = df_locs
                df_locs.reset_index(inplace=True)
                df_locs[["type", "date", "week_number", "gcc"]] = pd.DataFrame(
                    df_locs["index"].apply(eval).tolist()
                )

                df_locs.drop("index", axis=1, inplace=True)
            else:
                try:
                    with open(twitter_file) as f:
                        data = json.load(f)

                    # Convert the JSON data into a DataFrame
                    df_locs = pd.DataFrame.from_dict(data["docs"])
                    df_locs["type"] = df_locs["search_term"]
                    df_locs["date"] = pd.to_datetime(df_locs["timestamp"]).dt.date
                    df_locs["week_number"] = df_locs["week"]
                    df_locs["gcc"] = df_locs["gcc"]
                    df_locs = (
                        df_locs.groupby(["type", "date", "week_number", "gcc"])
                        .size()
                        .reset_index(name="value")
                    )
                    df_locs_group_by_week = (
                        df_locs.groupby(["type", "week_number", "gcc"])
                        .size()
                        .reset_index(name="value")
                    )

                except Exception as e:
                    print(f"An error occurred: {e}")

    except FileNotFoundError:
        print(f"Results topics file not found: {results_topics_file}")

    # ---Rate Data-----------------------
    if os.name == "nt":  # Check if the operating system is Windows
        result_target_rates_file = (
            f"{workdir}/flask_api/static/data/result_target_rates.json"
        )
    else:  # Assume it's a Unix-
        result_target_rates_file = f"{workdir}/static/data/result_target_rates.json"

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
    # interest_sample_df = df_rate.groupby('week_number').agg({'target_cash_rate':'max'}).reset_index()
    # ---inflation Data-----------------------
    if os.name == "nt":  # Check if the operating system is Windows
        result_inflations_file = (
            f"{workdir}/flask_api/static/data/result_inflations.json"
        )
    else:  # Assume it's a Unix-
        result_inflations_file = f"{workdir}/static/data/result_inflations.json"
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

    # convert the date column to datetime type
    # Make a copy of the DataFrame
    df_inflation_copy = df_locs.copy()

    # Convert the 'date' column to datetime type

    # Modify the 'date' column to the first day of each month
    # Rename the 'week_number' column to 'weekno'
    # df_inflation_copy = df_inflation_copy.rename(columns={'week_number': 'weekno'})

    interest_df = df_rate
    interest_df["date"] = pd.to_datetime(interest_df["date"], format="%d/%m/%Y")
    interest_df["week"] = interest_df["date"].dt.isocalendar().week
    interest_df["month"] = interest_df["date"].dt.month
    interest_sample_df = interest_df[
        (interest_df["date"] >= dt.datetime(2022, 2, 10))
        & (interest_df["date"] <= dt.datetime(2022, 8, 10))
    ]
    interest_sample_df = (
        interest_sample_df.groupby("week")
        .agg({"target_cash_rate": "max"})
        .reset_index()
    )

    inflation_df = df_inflation
    inflation_df["date"] = pd.to_datetime(inflation_df["date"], format="%d/%m/%Y")
    inflation_df["month"] = inflation_df["date"].dt.month
    inflation_sample_df = inflation_df[
        (inflation_df["date"] >= dt.datetime(2022, 2, 1))
        & (inflation_df["date"] <= dt.datetime(2022, 8, 10))
    ]
    inflation_sample_df = pd.merge(
        interest_df[["date", "week", "month"]],
        inflation_sample_df[["month", "cpi"]],
        on="month",
    )
    inflation_sample_df = inflation_sample_df.drop_duplicates("week")
    inflation_sample_df = inflation_sample_df[
        (inflation_sample_df["week"] > 5) & (inflation_sample_df["week"] < 33)
    ].reset_index()
    weekly_tweets_df = (
        df_tweets[df_tweets["topic"] == "interest rate"]
        .groupby("week")
        .agg({"id": "count"})
        .reset_index()
        .sort_values("week")
    )
    housing_weekly_tweets_df = (
        df_tweets[df_tweets["topic"] == "housing"]
        .groupby("week")
        .agg({"id": "count"})
        .reset_index()
        .sort_values("week")
    )
    inflation_weekly_tweets_df = (
        df_tweets[df_tweets["topic"] == "inflation"]
        .groupby("week")
        .agg({"id": "count"})
        .reset_index()
        .sort_values("week")
    )
    # convert the date column to datetime type
    weekly_tweets_df = weekly_tweets_df.rename(columns={"week": "Week"})
    housing_weekly_tweets_df = housing_weekly_tweets_df.rename(columns={"week": "Week"})
    inflation_weekly_tweets_df = inflation_weekly_tweets_df.rename(
        columns={"week": "Week"}
    )
    # join the two DataFrames on the date column
    interest_sample_df["RBA Rate"] = interest_sample_df["target_cash_rate"] * 100
    interest_sample_df = interest_sample_df.rename(columns={"week": "Week"})
    inflation_sample_df = inflation_sample_df.rename(columns={"week": "Week"})

    # Merge the weekly_tweets_df with interest_sample_df on 'Week'
    merged_df = pd.merge(
        weekly_tweets_df, interest_sample_df[["Week", "RBA Rate"]], on="Week"
    )
    inflation_merged_df = pd.merge(
        inflation_weekly_tweets_df, inflation_sample_df[["Week", "cpi"]], on="Week"
    )
    # Rename the columns
    merged_df = merged_df.rename(columns={"id": "Tweets"})
    inflation_merged_df = inflation_merged_df.rename(columns={"id": "Tweets"})

    # Prepare the data in the desired format
    InterestRaterises_vs_Tweet = {
        "meta": {"xLabel": "Week", "leftYLabel": "RBA Rate", "rightYLabel": "Tweets"},
        "data": merged_df.to_dict(orient="records"),
    }

    inflation_Tweet = {
        "meta": {"xLabel": "Week", "leftYLabel": "cpi", "rightYLabel": "Tweets"},
        "data": inflation_merged_df.to_dict(orient="records"),
    }

    # ----------End Rate--------------------------------------
    # ---Location Data---------------------------------------

    def get_location():
        if os.name == "nt":  # Check if the operating system is Windows
            result_locations_file = (
                f"{workdir}/flask_api/static/data/result_locations.json"
            )
        else:  # Assume it's a Unix-
            result_locations_file = f"{workdir}/static/data/result_locations.json"

        fetcher.save_Location_data()
        with open(result_locations_file) as f:
            location_data = json.load(f)

            if len(location_data) > 0:
                df_location = pd.DataFrame(
                    [
                        [eval(key)[0], eval(key)[1], eval(key)[2], eval(key)[3], value]
                        for key, value in location_data.items()
                    ],
                    columns=["Location", "gcc", "Coordinates", "date", "Count"],
                )

                df_location["date"] = pd.to_datetime(df_location["date"])
            else:
                try:
                    if os.name == "nt":  # Check if the operating system is Windows
                        twitter_file = f"{workdir}/flask_api/data/twitter/twitter.json"
                    else:  # Assume it's a Unix-
                        twitter_file = os.path.join(
                            f"{workdir}", "data", "twitter", "twitter.json"
                        )
                    with open(twitter_file) as f:
                        data = json.load(f)

                    # Convert the JSON data into a DataFrame
                    df_location = pd.DataFrame.from_dict(data["docs"])
                    # Convert the JSON data into a DataFrame

                    df_location["Location"] = df_location["location"]
                    df_location["date"] = pd.to_datetime(
                        df_location["timestamp"]
                    ).dt.date
                    df_location["Coordinates"] = df_location["coordinates"]
                    df_location["week_number"] = df_location["week"]
                    df_location["gcc"] = df_location["gcc"]
                    df_location = (
                        df_location.groupby(
                            ["Location", "date", "week_number", "Coordinates", "gcc"]
                        )
                        .size()
                        .reset_index(name="Count")
                    )
                    df_location_group_by_week = (
                        df_location.groupby(["Location", "week_number", "gcc"])
                        .size()
                        .reset_index(name="Count")
                    )

                except Exception as e:
                    print(f"An error occurred: {e}")

        return df_location

    # ----End Location------------------------

    df_loc_only = get_location()
    # df_rate["week_number"] = df_rate["week_number"].astype(int)

    # df_tweet_rate = pd.merge(df_loc_only, df_rate, on="week_number")

    # df_tweet_housing = pd.merge(
    #     df_inflation_copy[df_inflation_copy["type"] == "housing"],
    #     df_tweet_rate,
    #     on="week_number",
    # )

    # df_inflation["week_number"] = df_inflation["week_number"].astype(int)
    # df_tweet_inflation = pd.merge(
    #     df_inflation_copy[df_inflation_copy["type"] == "inflation"],
    #     df_inflation,
    #     on="week_number",
    # )

    # ----------End inflation--------------------------------------

    # ---income_mortgage Data-----------------------
    if os.name == "nt":  # Check if the operating system is Windows
        result_income_mortgages_file = (
            f"{workdir}/flask_api/static/data/result_income_mortgages.json"
        )
    else:  # Assume it's a Unix-
        result_income_mortgages_file = (
            f"{workdir}/static/data/result_income_mortgages.json"
        )

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

    df_income_mortgage = df_income_mortgage.rename(columns={"gcc_code16": "gcc"})
    df_income_mortgage["gcc"] = df_income_mortgage["gcc"].str.lower()

    # convert the date column to datetime type
    # Make a copy of the DataFrame

    df_grouped = df_loc_only.groupby("gcc")["Count"].sum().reset_index()

    # Convert the 'date' column to datetime type

    # Modify the 'date' column to the first day of each month
    # Rename the 'week_number' column to 'weekno'

    # df_income_mortgage_copy['weekno'] = df_income_mortgage_copy['date'].dt.isocalendar().week

    # df_income_mortgage['weekno'] = df_income_mortgage['date'].dt.isocalendar().week

    # Join the two DataFrames on the modified 'date' column
    df_tweet_income_mortgage = pd.merge(df_grouped, df_income_mortgage, on="gcc")

    # ----------End income_mortgage--------------------------------------

    # ---housing_total Data-----------------------
    if os.name == "nt":  # Check if the operating system is Windows
        result_housing_totals_file = (
            f"{workdir}/flask_api/static/data/result_housing_totals.json"
        )
    else:  # Assume it's a Unix-
        result_housing_totals_file = f"{workdir}/static/data/result_housing_totals.json"

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
    if os.name == "nt":  # Check if the operating system is Windows
        result_inequalitys_file = (
            f"{workdir}/flask_api/static/data/result_inequalitys.json"
        )
    else:  # Assume it's a Unix-
        result_inequalitys_file = f"{workdir}/static/data/result_inequalitys.json"
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

    grouped_df = df_locs.groupby(["gcc", "type"])["value"].sum().reset_index()

    df_loc_tweets_grouped = (
        df_locs.groupby(["week_number", "type"])["value"].sum().reset_index()
    )

    # Pivot the data to get the desired format
    pivot_df = pd.pivot_table(
        grouped_df, index="gcc", columns="type", values="value", aggfunc="sum"
    )

    pivot_df_by_week = pd.pivot_table(
        df_loc_tweets_grouped,
        index="week_number",
        columns="type",
        values="value",
        aggfunc="sum",
    )

    # Convert the pivot table to a dictionary in the desired format
    tweetsByTopicGrouped_arr = []
    tweetsByTopicGroupedByWeek_arr = []
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

    for index, row in pivot_df_by_week.iterrows():
        data_row = {
            "week_no": index,
            "housing": int(row["housing"]) if not pd.isna(row["housing"]) else 0,
            "inflation": int(row["inflation"]) if not pd.isna(row["inflation"]) else 0,
            "interestRate": int(row["interest rate"])
            if not pd.isna(row["interest rate"])
            else 0,
            "socialSecurity": int(row["social security"])
            if not pd.isna(row["social security"])
            else 0,
        }
        tweetsByTopicGroupedByWeek_arr.append(data_row)

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
            combined_df[f"{col}_pc"] = combined_df[col] / combined_df.earners_persons
    combined_df["rural_urban"] = combined_df["gcc"].apply(
        lambda gcc: fetcher.get_rural_urban(gcc)
    )
    # combined_df= combined_df.rename(columns={'U': 'metropolitan'})
    # combined_df= combined_df.rename(columns={'R': 'rural'})
    # ----------End inequality--------------------------------------

    # Tweets Sentiments----------------------------------

    # Assuming your DataFrame is called df
    sentiment_bins = [
        -float("inf"),
        -1,
        -0.75,
        -0.5,
        -0.25,
        0,
        0.25,
        0.5,
        0.75,
        1,
        float("inf"),
    ]
    bin_labels = [
        "-1<",
        "-0.75 / -0.50",
        "-0.50 / -0.25",
        "-0.25 / 0.00",
        "0.00 / 0.25",
        "0.25 / 0.50",
        "0.50 / 0.75",
        "0.75 / 1",
        ">1",
        "N/A",
    ]

    # Bin the sentiment values and calculate the frequencies
    df_tweets["sentiment_bin"], _ = pd.cut(
        df_tweets["sentiment"],
        bins=sentiment_bins,
        labels=False,
        retbins=True,
        include_lowest=True,
    )
    sentiment_freq = (
        df_tweets["sentiment_bin"].value_counts().sort_index().reset_index()
    )
    sentiment_freq.columns = ["bin", "frequency"]
    sentiment_freq["bin"] = bin_labels
    # Exclude the 'N/A' bin from the resulting data
    sentiment_freq = sentiment_freq[sentiment_freq["bin"] != "N/A"]
    sentiment_freq = sentiment_freq[sentiment_freq["bin"] != "-1<"]
    sentiment_freq = sentiment_freq[sentiment_freq["bin"] != ">1"]
    # Convert the frequencies to a list of dictionaries
    sentiment_data = sentiment_freq.to_dict("records")

    # Create the final dictionary
    twitter_sentiments = {"Label": "Twitter Sentiments", "data": sentiment_data}

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
                "xLabel": "week_no",
                "yLabel": "Tweets",
                "barLabels": ["housing", "inflation", "interestRate", "socialSecurity"],
            },
            "data": tweetsByTopicGroupedByWeek_arr,
        }

        # Serialize the final_data dictionary to JSON
        json_data = json.dumps(final_data)
        return json_data

    # df_tweet_rate=df_tweet_rate.groupby(["week_number", "target_cash_rate"])["Count"].sum().reset_index()
    @app.route("/targtRateByTweets")
    def targtRateByTweets():
        json_data = InterestRaterises_vs_Tweet
        return json_data

    # df_tweet_housing = df_tweet_housing.groupby(["week_number", "target_cash_rate"])[
    #     "Count"].sum().reset_index()

    # df_tweet_housing=df_tweet_housing.groupby(["week_number", "target_cash_rate"])["Count"].sum().reset_index()
    @app.route("/Housing_RBA_Related_Tweets")
    def Housing_RBA_Related_Tweets():
        data = {
            "meta": {
                "xLabel": "Week",
                "leftYLabel": "RBA Rate(Housing)",
                "rightYLabel": "Tweets",
            },
            "data": [],
        }

        # Iterate over the data and populate the 'data' list
        for index, row in interest_sample_df.iterrows():
            week = row["Week"]
            rba_rate = row["target_cash_rate"]
            tweets = housing_weekly_tweets_df[housing_weekly_tweets_df["Week"] == week][
                "id"
            ].values[0]

            data["data"].append(
                {
                    "Week": int(week),
                    "RBA Rate(Housing)": np.round(rba_rate, 8),
                    "Tweets": int(tweets),
                }
            )
        json_data = data
        return jsonify(json_data)

    # df_tweet_inflation["cpi"]=df_tweet_inflation["cpi"].round(3)
    # df_tweet_inflation=df_tweet_inflation.groupby(["week_number", "cpi"])["value"].sum().reset_index()

    @app.route("/inflationTweetsByDate")
    def inflationTweetsByDate():
        # data = {
        #     'meta': {
        #         'xLabel': 'Week',
        #         'leftYLabel': 'Inflation',
        #         'rightYLabel': 'Tweets'
        #     },
        #     'data': []
        # }

        # for index, row in weekly_tweets_df.iterrows():
        #     week_data = {
        #         "Week": row["week"],
        #         "Inflation": inflation_sample_df[
        #             inflation_sample_df["Week"] == row["Week"]
        #         ]["cpi"].values[0],
        #         "Tweets": row["id"],
        #     }
        #     data['data'].append(week_data)
        for item in inflation_Tweet["data"]:
            item["cpi"] = item["cpi"].replace("%", "")
        json_data = inflation_Tweet
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

    combined_df["interestRate_pc"] = combined_df["interestRate_pc"].round(2)

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
            grouped_df_ru["interestRate_pc"] = grouped_df_ru["interestRate_pc"].round(2)
            grouped_df_ru["own_outright_total_pc"] = grouped_df_ru[
                "own_outright_total_pc"
            ].round(2)
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

    # @app.route("/targtRateByDate")
    # def targtRateByDate():
    #     if df_rate["date"].notnull().all():
    #         df_rate["date"] = pd.to_datetime(df_locs["date"])
    #         df_rate["date"] = df_rate["date"].dt.strftime("%Y-%m-%d")
    #     return df_rate.to_json(orient="records")

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
        grouped_data = df_tweets.groupby("gcc").size().to_dict()

        result = [{"gcc": gcc, "tweets": count} for gcc, count in grouped_data.items()]

        return result

    @app.route("/tweetSentimentAnalysis")
    def tweetSentimentAnalysis():
        formatted_data = twitter_sentiments

        return jsonify(formatted_data)

    import time

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
    # Save the toot data
    fetcher = FetcherHarverster(
        args.couchdb_master_ip, args.couchdb_username, args.couchdb_password
    )

    @app.route("/tootSentimentAnalysis")
    def tootSentimentAnalysis():
        # Fetch toots

        # Set the result_toots_file path based on the operating system
        if os.name == "nt":  # Check if the operating system is Windows
            result_toots_file = f"{workdir}/flask_api/static/data/result_toots.json"
        else:  # Assume it's a Unix-like system
            result_toots_file = f"{workdir}/static/data/result_toots.json"

        fetcher.save_toot_data()

        # Load the toot data from the result_toots_file
        with open(result_toots_file) as f:
            toot_data = json.load(f)

        formatted_data = {
            "mastodonSentiments": {
                "Label": "Mastodon Sentiments",
                "data": [
                    {"bin": bin_key, "frequency": frequency}
                    for bin_key, frequency in toot_data.items()
                ],
            }
        }

        return jsonify(formatted_data)

    # ----End toot------------------------

    return app


if __name__ == "__main__":
    FE_DDOMAIN_DEV = "http://localhost:3000"
    # process_mastadon=Process_Mastodon()
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

    # parser.add_argument("--ado_api_key", help="api key for ado server" ,default="a2a6e2f96a2c94a04661aacc6e394caa")
    # parser.add_argument("--ado_login_url", help="ado api login url",default="https://api.ado.eresearch.unimelb.edu.au/login")
    # parser.add_argument("--ado_text_search_mastodon_url", help="ado api text search url for mastodon",default="https://api.ado.eresearch.unimelb.edu.au/analysis/textsearch/collections/mastodon")
    # parser.add_argument("--mastodon_api_key", help="api key for the mastodon server",default="f8-yNpSEGxPcQwwz_GxYtET3VumoGZ6KAQAH6bybICE")
    args = parser.parse_args()
    # process=Process_Mastodon( args.ado_api_key, args.ado_login_url, args.ado_text_search_mastodon_url,args.mastodon_api_key)
    fetcher2 = FetcherHarverster(
        args.couchdb_master_ip, args.couchdb_username, args.couchdb_password
    )

    fetcher = Fetcher(
        args.couchdb_master_ip, args.couchdb_username, args.couchdb_password
    )

    app = pre_task(fetcher=fetcher)
    #cors = CORS(app, resources={r"/*": {"origins": FE_DDOMAIN_DEV}})
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    #app.run(debug=True, use_reloader=True)
    app.run(host="0.0.0.0", port=5000

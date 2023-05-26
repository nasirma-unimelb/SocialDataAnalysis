# COMP90024 - ASSIGNMENT 2 / Back_End

## Introduction
This repository contains the back-end code for Group 1's project. The main purpose of the back-end is to handle the storage, retrieval, and exposure of data from CouchDB through API endpoints using the Python Flask library.

## Technologies
This project is built using Python, along with the following libraries and tools:

+ fortawesome/fontawesome-svg-core: ^6.4.0
+ argparse: ^1.4.0
+ couchdb: ^1.2
+ flask: ^2.3.2
+ pandas: ^2.0.1
+ flask_cors: ^3.0.10
+ textblob: ^0.17.1
+ requests: ^2.30.0
+ mastodon.py: ^1.8.1
+ numpy: ^1.24.3

## Features
The following API endpoints are available and can be tested using Postman or cURL:

+ "/tweetSentimentAnalysis" (GET): Provides details about tweet sentiments and presents the results in the form of bins.
+ "/tootSentimentAnalysis" (GET): Provides details about Mastodon toot sentiments and presents the results in the form of bins.
+ "/own_outright_vs_mortgage" (GET): Provides details about the relationship between interest rates and home ownership (outright vs mortgage).
+ "/larger_mortgage_with_interestRate_By_Sentiment" (POST): Provides details about the relationship between interest rates and home ownership based on mortgage and location. The results are grouped by rural vs urban and filtered by "sentiment" from the UI.
+ "/larger_mortgage_with_interestRate" (GET): Provides details about the relationship between interest rates and home ownership based on mortgage and location. The results are grouped by rural vs urban.
+ "/Housing_RBA_Related_Tweets" (GET): Provides details about the relationship between interest rates and the volume of tweets related to housing topics. The results are grouped by week.
+ "/targtRateByTweets" (GET): Provides details about the relationship between interest rates and the volume of tweets related to interest rate topics. The results are grouped by week.
+ "/tweetsByTopicGrouped_By_Sentiment" (POST): Provides details about the relationship between the volume of tweets related to different topics and grouped by week. The results are filtered by "sentiment" from the UI.
+ "/tweetsByTopicGrouped" (GET): Provides details about the relationship between the volume of tweets related to different topics and grouped by week.
+ "/inflationTweetsByDate" (GET): Provides details about the relationship between inflation and the volume of tweets related to inflation topics. The results are grouped by week.

## Installation
To run this program, you will need to follow these steps:

1. Install Python 3.11.3 or above.
2. Run `pip install` from the root directory to install the dependencies specified in the "requirements.txt" file.
3. Place all the static files in the following paths: "/data/other" and "/data/twitter".
4. Run `python back_end_exposer.py` to start the back-end server, which will be running by default on port 5000.

## Docker
In the root directory, you will find a Dockerfile that can be used to build a Docker image for automated deployment.

## Group Members
+ Mohammed Nasir: 1345586
+ Elena Pashkina: 1141034
+ Ellen Morwitch: 1257182
+ Felipe Leefu Huang Lin: 1202652
+ Nicholas Barry: 587667
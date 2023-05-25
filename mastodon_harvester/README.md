# COMP90024 - ASSIGNMENT 2 / DASHBOARD

## Introduction:
Git repository for group 1 project's Mastodon Harvester. The Harvester pulls toots from the ADO api and send them to be stored on a CouchDB cluster. They are passed to the front-end application by a backend intermediary.

## Technologies:
This project was built using Python.


## Instalation: 
This project was built on an Ubuntu 22.04 OS. To run this program you will need to install:
+ Pyython 3.x
+ Run `pip install -r requirements.txt` from this directory
+ Enter the coucdb IP, username and password to connect with. They are passed as command line arguments.
+ Run `python3 mastodon_harvester.py`
## Docker:
In the `mastodon_harvester` directory there is a Dockerfile used to build docker image for automated deployment.

## Group Members:
+ Mohammed Nasir:1345586
+ Elena Pashkina:1141034
+ Ellen Morwitch: 1257182
+ Felipe Leefu Huang Lin: 1202652
+ Nicholas Barry: 587667
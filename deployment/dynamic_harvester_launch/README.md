# COMP90024 - ASSIGNMENT 2 / DASHBOARD

## Introduction:
Git repository for group 1 project's automatic Mastodon Harvester virtual machine launch. The system launchs one virtual machine. The machine allows the system to scale dynamically with the volume, velocity and variety of toots that is required.

## Technologies:
This project was built using Ansible and its openstackSDK modules as well as Docker for containerisation.


## Installation: 
This project was built on an Ubuntu 22.04 OS. To run this program you will need to install:
+ Python > 3.11
+ ansible ==7.5.0
+ ansible-core == 2.14.5
+ openstack.cloud 2.1.0 (ansible collection)
+ OpenstackSDK 1.2.0
+ Place your `openrc.sh` file in the system_launch directory.
+ Configure the path to your ssh key file in the `hosts` file
+ Run `run-all-in-one.sh` from a terminal window
+ Enter your Openstack password when prompted

## Group Members:
+ Mohammed Nasir:1345586
+ Elena Pashkina:1141034
+ Ellen Morwitch: 1257182
+ Felipe Leefu Huang Lin: 1202652
+ Nicholas Barry: 587667
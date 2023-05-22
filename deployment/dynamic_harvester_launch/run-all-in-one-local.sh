#!/usr/bin/env bash

. ./openrc.sh; source /home/nickbarry/Documents/MsC-DS/Cluster_and_Cloud_Comuting-COMP90024/Assignments/A2/comp90024-a2/venv311/bin/activate; ansible-playbook -vvvv -i hosts all-in-one.yaml | tee output.txt

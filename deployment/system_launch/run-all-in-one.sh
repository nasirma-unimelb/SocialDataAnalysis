#!/usr/bin/env bash

. ./openrc.sh; ansible-playbook -vvvv -i hosts all-in-one.yaml | tee output.txt

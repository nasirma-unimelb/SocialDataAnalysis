#!/usr/bin/env bash

. ./comp90024-openrc.sh; ansible-playbook -vv -i hosts all-in-one.yaml | tee output.txt

import harvester_dep
import sys
import requests
import subprocess

if __name__ == "__main__":
    print("Running main")
    harvester_dep.harvest()
    print("Imported from /harvester")
    print(sys.argv)
    if sys.argv[-1] == "post":
        print("posting")
        command = 'curl -X PUT "http://admin:admin@172.26.135.12:5984/twitter/adam" --header "Content-Type:application/json" --data \'{"type": "account", "holder": "Charlie","initialbalance": 100}\''
        subprocess.run(command, shell=True)
        print("posted")

# Ansible Playbook
This automates the entire IT process from instance creation to app deployment on Melbourne Research Cloud.

## Setup
- Python-3 needs to be installed locally
- You need to have Ansible installed locally
- You will have to get your own Openstackrc file along with a openstack api password

## Execution
- To run the ansible script, run the command <br/>```. ./unimelb-comp90024-2023-grp-01-openrc.sh; ansible-playbook -i inventory/inventory.ini mrc.yaml```

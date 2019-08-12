# VLANs-Tool
Create, Modify, Delete and Sync Vlans between Switch and sql Database


1-
#######MySQL SETUP#######
apt-get install software-properties-common  python-dev build-essential libssl-dev libffi-dev  libxml2-dev python3-dev libxslt1-dev zlib1g-dev less -y
apt-get install mariadb-client-core-10.3
service mysql start
mysql -u root -p
Enter password: (blank password)


2-
apt-get install python3 python3-pip python3-virtualenv python3-venv -y

virtualenv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

3-
python3 vlan-tool.py


4- After typing switch & sql ips + credentials the below list will the show up

Use this tool to:
a - Sync-To(From MYSQL to Sw)
b - Sync-From(From Sw to SQL)
c - Create VLAN
d - update vlan
e - delete vlan
f - Connect Another Device
g - Exit program
choose(a, b, c, d, e)
Enter your choice:


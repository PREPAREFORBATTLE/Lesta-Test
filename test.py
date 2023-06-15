#!/usr/bin/python
import paramiko
import os
import json

x = """
{
    "hosts": {
        "EU-CLUSTER": {
            "title": "Eu cluster discription",
            "host": "eu1-vm-host",
            "user": "euuser"
        },
        "NA-CLUSTER": {
            "title": "Na cluster description",
            "host": "na1-vm-host",
            "user": "nauser"
        }
    }
}
"""

data = json.loads(x)

for datas in data["hosts"]:
    hostName = data["hosts"][datas]["host"]
    UserName = data["hosts"][datas]["user"]
    if "key" in data["hosts"][datas]:
        pkey = paramiko.RSAKey.from_private_key_file(data["hosts"][datas]["key"])
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostName, username=UserName, pkey=pkey)
	else
		client.connect(hostName, username=UserName, password=UserName)
	stdin, stdout, stderr = client.exec_command('cd ~/bw/; git branch')
	if stderr is None:
		branch = stdout.read().strip("\n")
		stdin, stdout, stderr = client.exec_command('cd ~/bw/; git rev-parse HEAD')
		rev = stdout.read().strip("\n")
	else
		stdin, stdout, stderr = client.exec_command('cd ~/bw/; svn info | grep '^URL:' | egrep -o '(tags|branches)/[^/]+' | egrep -o '[^/]+$'')
		branch = stdout.read().strip("\n")
		stdin, stdout, stderr = client.exec_command('cd ~/bw/; svn info | grep '^Revision:' | egrep -o '[^:]+$'')
		rev = stdout.read().strip("\n")
	newData = {"Rev": rev, "Branche": branch}
	data["hosts"][datas].update(newData)
print(json.dumps(data, indent=4))
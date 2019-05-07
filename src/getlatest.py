import json
import os
import urllib.request


npmRank = "assets/npmRank.json"
with open(npmRank, "r") as read_file:
    data = json.load(read_file)
    for index, package in enumerate(data):
        npmUrl = "https://registry.npmjs.org/" + data[index]["packageName"]
        print ("Processing->  ", data[index]["packageName"])
        with urllib.request.urlopen(npmUrl) as url:
            npmReg = json.loads(url.read().decode())
            print (npmReg["dist-tags"]["latest"])
            data[index]["latest"] = npmReg["dist-tags"]["latest"]
    with open("assets/latetVer.json", 'w') as outfile:
        json.dump(data, outfile)

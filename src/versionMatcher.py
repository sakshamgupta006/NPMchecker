import urllib.request
import json
import pprint
import os

#get the version from npm registry
repoName = "winston"
owner = "winstonjs"
githubUrl = "https://github.com/winstonjs/winston.git"
testUrl = "https://registry.npmjs.org/" + repoName

with urllib.request.urlopen(testUrl) as url:
    npmReg = json.loads(url.read().decode())
    githubApi = "https://api.github.com/repos/" + owner + "/" + repoName + "/tags"
    with urllib.request.urlopen(githubApi) as urlGithub:
        githubData = json.loads(urlGithub.read().decode())
        for version in npmReg["versions"]:
            version.encode("utf-8")
            # print (version)
            for index, value in enumerate(githubData):
                if githubData[index]["name"] == ((version) or ("v" + version)):
                    print (version, "Matched")
        # print ("Github Versions")
        # for index, value in enumerate(githubData):
        #     print (githubData[index]["name"])

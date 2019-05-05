import urllib.request
import json
import pprint
import os

#get the version from npm registry
repoName = "graphql-js"
owner = "graphql"
githubUrl = "https://github.com/graphql/graphql-js.git"
testUrl = "https://registry.npmjs.org/" + owner

with urllib.request.urlopen(testUrl) as url:
    npmReg = json.loads(url.read().decode())
    githubApi = "https://api.github.com/repos/" + owner + "/" + repoName + "/tags"
    with urllib.request.urlopen(githubApi) as urlGithub:
        githubData = json.loads(urlGithub.read().decode())
        for version in npmReg["versions"]:
            version.encode("utf-8")
            # print (version)
            for index, value in enumerate(githubData):
                if githubData[index]["name"] == (version) or githubData[index]["name"] == ("v" + version):
                    print (version, "Matched")
        # print ("Github Versions")
        # for index, value in enumerate(githubData):
        #     print (githubData[index]["name"])

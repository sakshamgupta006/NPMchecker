import urllib.request
import json
import pprint

#get the version from npm registry
repoName = "lodash"
testUrl = "https://registry.npmjs.org/" + repoName
with urllib.request.urlopen(testUrl) as url:
    npmReg = json.loads(url.read().decode())
    # githubApi = "https://api.github.com/repos/" + repoName + "/" + repoName + "/tags"
    # with urllib.request.urlopen(githubApi) as urlGithub:
    # githubData = json.loads(urlGithub.read().decode())
    with open("lodashapi.json", "r") as read_file:
        githubData = json.load(read_file)
        for version in npmReg["versions"]:
            version.encode("utf-8")
            for index, value in enumerate(githubData):
                if githubData[index]["name"] == version:
                    print (version, "Matched")

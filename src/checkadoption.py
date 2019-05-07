import json
import os
import pprint
import io
import urllib.request
import requests

githubUrl = "assets/npmGithubUrl.json"
currentCounter = 0
nourl_counter = 0
repos_with_build = 0
repos_with_no_build = 0
repos_not_cloned = 0
packages_with_build = []
packages_with_no_package = []
total_latest_packages = 0
total_old_packages = 0
packages_processed = 0
with open(githubUrl, "r") as read_file:
    data = json.load(read_file)
    for index, repo in enumerate(data):
        latest_packages_count = 0
        old_packages_count = 0
        currentCounter += 1
        print ("Processing: ", data[index]["packageName"])
        packageSplit = data[index]["packageName"].split("/")
        if len(packageSplit) == 1:
            if "githubUrl" not in data[index]:
                print ("No Github URL found")
                nourl_counter += 1
            else:
                print (data[index]["githubUrl"])
                #Download the latest repository and check if it has a build script
                cloneCommand = "git clone " + data[index]["githubUrl"]
                os.system(cloneCommand)

                #Break the URl to get clone directory
                splitUrl = data[index]["githubUrl"].split("/")
                currentDirectory = splitUrl[-1]
                #Remove .git from end
                currentDirectory = currentDirectory[:-4]

                #check in the repository
                currentJson = currentDirectory + "/package.json"
                exists = os.path.isfile(currentJson)
                newVersionDict = {}
                if exists:
                    packages_processed += 1
                    with open(currentJson, "r") as read_package:
                        dataPackage = json.load(read_package)
                        if "devDependencies" in dataPackage:
                            packageDict = dataPackage["devDependencies"]
                            newVersionDict["package"] = data[index]["packageName"]
                            newVersionDict["latest"] = {}
                            newVersionDict["old"] = {}
                            for dependent, ver in packageDict.items():
                                #Check for the latest and Matched
                                #Search for package in Top 1000
                                checklatestUrl = "https://registry.npmjs.org/" + dependent
                                request = requests.get(checklatestUrl)
                                if request.status_code == 200:
                                    with urllib.request.urlopen(checklatestUrl) as url:
                                        npmReg = json.loads(url.read().decode())
                                        if "dist-tags" in npmReg:
                                            if "latest" in npmReg["dist-tags"]:
                                                latestVer = npmReg["dist-tags"]["latest"]
                                                #Modify ver to match with latestVersion
                                                if ver[0] == "^":
                                                    #Match till first
                                                    splitsubVersionsCurrent = ver.split(".")
                                                    splitsubVersionsLatest = latestVer.split(".")
                                                    if splitsubVersionsCurrent[0][1:] == splitsubVersionsLatest[0]:
                                                        latest_packages_count += 1
                                                        newVersionDict["latest"][dependent] = latestVer
                                                    else:
                                                        old_packages_count += 1
                                                        newVersionDict["old"][dependent] = ver[1:]
                                                elif ver[0] == "~":
                                                    #Match till second
                                                    splitsubVersionsCurrent = ver.split(".")
                                                    splitsubVersionsLatest = latestVer.split(".")
                                                    if splitsubVersionsCurrent[0][1:] == splitsubVersionsLatest[0] and splitsubVersionsCurrent[1] == splitsubVersionsLatest[1]:
                                                        latest_packages_count += 1
                                                        newVersionDict["latest"][dependent] = latestVer
                                                    else:
                                                        old_packages_count += 1
                                                        newVersionDict["old"][dependent] = ver[1:]
                                                else:
                                                    #Match full versions
                                                    if ver == latestVer:
                                                        latest_packages_count += 1
                                                        newVersionDict["latest"][dependent] = latestVer
                                                    else:
                                                        old_packages_count += 1
                                                        newVersionDict["old"][dependent] = ver
                            newVersionDict["latest"]["count"] = latest_packages_count
                            total_latest_packages += latest_packages_count
                            total_old_packages += old_packages_count
                            print ("Latest Versions: ", latest_packages_count)
                            print ("Old Versions: ", old_packages_count)
                            newVersionDict["old"]["count"] = old_packages_count
                    jsonSavePath = data[index]["packageName"] + ".json"
                    with open(jsonSavePath, 'w') as outfile:
                        json.dump(newVersionDict, outfile)
                else:
                    repos_not_cloned += 1

                #Remove the downloaded directory
                os.system("rm -rfd " + currentDirectory)
        # if currentCounter > 3:
        #     break

print ("Repos without URL: ", nourl_counter)
print ("Repos not cloned", repos_not_cloned)
print ("Repos with build: ", repos_with_build)
print ("Repos with no build: ", repos_with_no_build)
print ("Total Latest Packages: ", total_latest_packages)
print ("Total Old Packages: ", total_old_packages)
print ("Total Packages Processed: ", packages_processed)

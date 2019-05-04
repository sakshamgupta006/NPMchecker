import json
import os
import pprint
import io

githubUrl = "../assets/npmGithubUrl.json"
currentCounter = 0
nourl_counter = 0
repos_with_build = 0
repos_with_no_build = 0
repos_not_cloned = 0
packages_with_build = []
with open(githubUrl, "r") as read_file:
    data = json.load(read_file)
    for index, repo in enumerate(data):
        currentCounter += 1
        print ("Processing: ", data[index]["packageName"])
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
            if exists:
                with open(currentJson, "r") as read_package:
                    dataPackage = json.load(read_package)
                    if "scripts" in dataPackage:
                        if "build" not in dataPackage["scripts"]:
                            repos_with_no_build += 1
                        else:
                            repos_with_build += 1
                            packages_with_build.append(data[index]["packageName"])
                            print (packages_with_build)
            else:
                repos_not_cloned += 1

            #Remove the downloaded directory
            os.system("rm -rfd " + currentDirectory)
        # if currentCounter > 3:
        #     break

print (packages_with_build)
print ("Repos without URL: ", nourl_counter)
print ("Repos not cloned", repos_not_cloned)
print ("Repos with build: ", repos_with_build)
print ("Repos with no build: ", repos_with_no_build)

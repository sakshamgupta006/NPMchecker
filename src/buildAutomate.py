import urllib.request
import json
import pprint
import os
from bs4 import BeautifulSoup
import re
import requests

# Function to extract score from comment
def extractStringBetweenTwoCharacters(line, nameStart, nameEnd):
    if line.find("score") != -1:
        substr = (line.split(nameStart))[1].split(nameEnd)[0]
        return substr
    return -1

def createScoreHash(scoreList):
    scoreHash = {}
    count = 1
    total = 0

    for score in scoreList:
        scoreHash[count] = int(score)
        total += int(score)
        count += 1

    if count == 1:
        return scoreHash, 0, 0

    count -= 1
    average = total/count
    scoreHash['differentFileCount'] = count
    scoreHash['averageScore'] = average

    return scoreHash, count, average

packName = "sinon"

packageList = ['clipboard', 'localforage', 'es6-error', 'preact', 'vue-resource', 'immutability-helper', 'react-error-overlay', 'angular-ui-router', 'tslint-react', 'husky', 'ts-jest', 'hexlet-pairs', 'bytebuffer', 'rc-slider', 'ua-parser-js', 'awesome-typescript-loader', 'object.assign', 'dom-helpers', 'raven', 'sanitize-html', 'intl', 'postcss-preset-env', 'blueimp-md5', 'base64-js', 'big.js', 'karma-webpack', 'toml', 'common-tags', 'bitcoinjs-lib', 'ignore', 'babel-plugin-named-asset-import', 'react-onclickoutside']

for package in packageList:
    print ("Current Package--> ", package)
    with open("assets/npmGithubUrl.json", "r") as main_file:
        mainFile = json.load(main_file)
        for ind, val in enumerate(mainFile):
            if package == mainFile[ind]["packageName"]:
                #get the version from npm registry
                repoName = ""
                owner = ""
                githubUrl = ""
                testUrl = ""
                finalScore = 0
                finalCount = 0
                repos_with_no_build = 0
                repos_with_build = 0
                #get owner and package from previously populated URl
                with open("assets/npmGithubUrl.json", "r") as read_file:
                    npmGit = json.load(read_file)

                    #Find the pakage in the packages
                    for index, value in enumerate(npmGit):
                        if package == npmGit[index]["packageName"]:
                            githubUrl = npmGit[index]["githubUrl"]
                            # testUrl = npmGit[index]["npmUrl"]
                            testUrl = "https://registry.npmjs.org/" + package

                            #Find the OWNER
                            splitGithub = githubUrl.split("/")
                            owner = splitGithub[-2]
                            repoName = splitGithub[-1][:-4]
                            print (repoName)
                            print (owner)
                            print (githubUrl)
                            print (testUrl)

                # Make the repo folders
                os.system("mkdir " + repoName)

                # Make the github and npm folders
                os.system("mkdir " + repoName + "/" + repoName + "Git " + repoName + "/" + repoName + "NPM")
                os.system("mkdir " + repoName + "/" + repoName + "builtGit")
                os.system("mkdir " + repoName + "/" + repoName + "diffOut")

                #Clone into the github folder
                cloneCommand = "git clone " + githubUrl + " " + repoName + "/" + repoName + "Git"
                os.system(cloneCommand)

                totalRepoCount = 0

                with urllib.request.urlopen(testUrl) as url:
                    npmReg = json.loads(url.read().decode())

                    #CHANGE IF THE OWNER IS DIFFERENT
                    githubApi = "https://api.github.com/repos/" + owner + "/" + repoName + "/tags"

                    with urllib.request.urlopen(githubApi) as urlGithub:
                        githubData = json.loads(urlGithub.read().decode())
                        # with open("lodashapi.json", "r") as read_file:
                        #     githubData = json.load(read_file)
                        for version in npmReg["versions"]:
                            version.encode("utf-8")
                            # print (version)
                            for index, value in enumerate(githubData):
                                # print (githubData[index]["name"])
                                if githubData[index]["name"] == (version) or githubData[index]["name"] == ("v" + version):
                                    print (version, "Matched")
                                    print ("Processing...")
                                    buildCurrent = True
                                    #Checkout to that sha
                                    currentSHA = githubData[index]["commit"]["sha"]
                                    os.system("git -C " + repoName + "/" + repoName + "Git checkout " + currentSHA)

                                    #check in the repository
                                    currentJson = repoName + "/" + repoName + "Git/package.json"
                                    exists = os.path.isfile(currentJson)
                                    if exists:
                                        with open(currentJson, "r") as read_package:
                                            dataPackage = json.load(read_package)
                                            if "scripts" in dataPackage:
                                                if "build" not in dataPackage["scripts"]:
                                                    repos_with_no_build += 1
                                                    buildCurrent = False
                                                else:
                                                    repos_with_build += 1
                                                    buildCurrent = True

                                    # Build only if build script exists
                                    if buildCurrent:
                                        totalRepoCount += 1
                                        #Build the git npm
                                        os.system("npm install --prefix " + repoName + "/" + repoName + "Git/")
                                        os.system("npm run build --prefix " + repoName + "/" + repoName + "Git/")

                                        #Commit the dist folders away
                                        os.system("git " + "-C " + repoName + "/" + repoName + "Git" +  " add .")
                                        os.system("git " + "-C " + repoName + "/" + repoName + "Git" +  " commit -m \"Buit the version\"")

                                        #Take the package folder out of the main github repo
                                        os.system("mkdir " + repoName + "/" + repoName + "builtGit/" + version)
                                        # CHANGE THE DIST FOLDER TO PACKAGE IF NECESSARY
                                        os.system("cp -r " + repoName + "/" + repoName + "Git/dist " + repoName + "/" + repoName + "builtGit/" + version)
                                        os.system("cp -r " + repoName + "/" + repoName + "Git/lib " + repoName + "/" + repoName + "builtGit/" + version)
                                        os.system("cp -r " + repoName + "/" + repoName + "Git/built " + repoName + "/" + repoName + "builtGit/" + version)

                                        #Make tar of the version
                                        os.system("tar -czvf " + repoName + "/" + repoName + "builtGit/" + version + ".tgz -C " + repoName + "/" + repoName + "builtGit/" + version + " .")

                                        #Delete the main builtGit
                                        os.system("rm -rdf " + repoName + "/" + repoName + "builtGit/" + version)

                                        #Download the npm registry repo as well
                                        versionDir = "mkdir " + repoName + "/" + repoName + "NPM/" + version
                                        os.system(versionDir)

                                        #Download the dist file in the folder
                                        tarUrl = npmReg["versions"][version]["dist"]["tarball"]
                                        request = requests.get(tarUrl)
                                        if request.status_code == 200:
                                            downloadTar = "wget -O " + repoName + "/" + repoName + "NPM/" + version + ".tgz " + tarUrl
                                            os.system(downloadTar)

                                            # Run trydiffoscope on the
                                            os.system("mkdir " + repoName + "/" + repoName + "diffOut/" + version)
                                            os.system("trydiffoscope --html " + repoName + "/" + repoName + "diffOut/" + version + "/" + repoName + "_" + version + ".html "
                                            + repoName + "/" + repoName + "builtGit/" + version + ".tgz " + repoName + "/" + repoName + "NPM/" + version + ".tgz")

                                            print ("Diffoscope Completed...")
                                            
                                            #Find the score of the differences
                                            htmlUrl = repoName + "/" + repoName + "diffOut/" + version + "/" + repoName + "_" + version + ".html"
                                            page = open(htmlUrl)
                                            soup = BeautifulSoup(page.read(), "lxml")

                                            # Find all comments in the html file
                                            comments = soup.find_all('div', {'class':'comment'})
                                            scores = []

                                            for comment in comments:
                                                #print (comment)
                                                score = extractStringBetweenTwoCharacters(str(comment), '(score: ', ',')
                                                if score != -1:
                                                    scores.append(score)

                                            diffScoreJson, currentCount, currentScore = createScoreHash(scores)
                                            finalCount += currentCount
                                            finalScore += currentScore
                                            jsonSavePath = repoName + "/" + repoName + "diffOut/" + version + "/" + repoName + "_" + version + ".json"
                                            with open(jsonSavePath, 'w') as outfile:
                                                json.dump(diffScoreJson, outfile)

                                            os.system("rm -rdf " + repoName + "/" + repoName + "NPM/" + version)

                                    #Extract tar
                                    # ExtractTar = "tar xvzf " + repoName + "/" + repoName + "NPM/" + version + ".tgz" + " -C " + repoName + "/" + repoName + "NPM/" + version + "/"
                                    # os.system(ExtractTar)
                                    #
                                    # #Delete the tar
                                    # os.system("rm -rf " + repoName + "/" + repoName + "NPM/" + version + ".tgz")
                                    #
                                    # print ("Tar Extraction Completed -> ", version)

                os.system("rm -rdf " + repoName + "/" + repoName + "Git")
                print ("Final Count --->>>> ", finalCount)
                print ("Final Score --->>>> ", finalScore)
                if totalRepoCount != 0:
                    print ("Final Score Avg --->>> ", finalScore/totalRepoCount)
                print("Total Repo Count --->>> ", totalRepoCount)
                print ("Total Repo with no build --->>> ", repos_with_no_build)
                print ("Total Repo with build --->>> ", repos_with_build)

                mainDict = {}
                mainDict["FinalCount"] = finalCount
                mainDict["finalScore"] = finalScore
                if totalRepoCount != 0:
                    mainDict["FinalAvgScore"] = finalScore/totalRepoCount
                else:
                    mainDict["FinalAvgScore"] = 0
                mainDict["totalRepoCount"] = totalRepoCount
                mainDict["RepoNotBuilt"] = repos_with_no_build
                mainDict["ReposBuilt"] = repos_with_build
                mainjsonSave = repoName + "/" + "result_" + repoName + ".json"
                with open(mainjsonSave, 'w') as outfile:
                    json.dump(mainDict, outfile)

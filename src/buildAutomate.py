import urllib.request
import json
import pprint
import os

#get the version from npm registry
packName = "es6-promisify"
repoName = ""
owner = ""
githubUrl = ""
testUrl = ""
#get owner and package from previously populated URl
with open("assets/npmGithubUrl.json", "r") as read_file:
    npmGit = json.load(read_file)

    #Find the pakage in the packages
    for index, value in enumerate(npmGit):
        if packName == npmGit[index]["packageName"]:
            githubUrl = npmGit[index]["githubUrl"]
            # testUrl = npmGit[index]["npmUrl"]
            testUrl = "https://registry.npmjs.org/" + packName

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

#Clone into the github folder
cloneCommand = "git clone " + githubUrl + " " + repoName + "/" + repoName + "Git"
os.system(cloneCommand)

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
                    #Checkout to that sha
                    currentSHA = githubData[index]["commit"]["sha"]
                    os.system("git -C " + repoName + "/" + repoName + "Git checkout " + currentSHA)

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

                    #Download the npm registry repo as well
                    versionDir = "mkdir " + repoName + "/" + repoName + "NPM/" + version
                    os.system(versionDir)

                    #Download the dist file in the folder
                    tarUrl = npmReg["versions"][version]["dist"]["tarball"]
                    downloadTar = "wget -O " + repoName + "/" + repoName + "NPM/" + version + ".tgz " + tarUrl
                    os.system(downloadTar)

                    #Extract tar
                    ExtractTar = "tar xvzf " + repoName + "/" + repoName + "NPM/" + version + ".tgz" + " -C " + repoName + "/" + repoName + "NPM/" + version + "/"
                    os.system(ExtractTar)

                    #Delete the tar
                    os.system("rm -rf " + repoName + "/" + repoName + "NPM/" + version + ".tgz")

                    print ("Tar Extraction Completed -> ", version)

os.system("rm -rdf " + repoName + "/" + repoName + "Git")

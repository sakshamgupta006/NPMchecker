import json
import os

repoName = "lodash"
testUrl = "https://registry.npmjs.org/" + repoName

#Download the json file into the repo folder
directoryRepoCommand = "mkdir " + repoName
os.system(directoryRepoCommand)

downloadCommand = "wget -O " + repoName + "/" + repoName + ".json " + testUrl
os.system(downloadCommand)

#Parse the json to download the version
jsonRepoName = repoName + "/" + repoName + ".json"
with open(jsonRepoName, "r") as read_file:
	data = json.load(read_file)
	for version in data["versions"]:
		version.encode("utf-8")
		print "Starting -> ", version
		#make directory of the version
		versionDir = "mkdir " + repoName + "/" + version
		os.system(versionDir)

		#Download the dist file in the folder
		tarUrl = data["versions"][version]["dist"]["tarball"]
		downloadTar = "wget -O " + repoName + "/" + version + "/" + version + ".tgz " + tarUrl
		os.system(downloadTar)

		#Extract tar
		ExtractTar = "tar xvzf " + repoName + "/" + version + "/" + version + ".tgz" + " -C " + repoName + "/" + version + "/" 
		os.system(ExtractTar)
		print "Completed -> ", version
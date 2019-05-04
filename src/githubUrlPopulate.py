import json
import os
import pprint
import io

npmRank = "../assets/npmRank.json"
noUrlCount = 0
with open(npmRank, "r") as read_file:
	data = json.load(read_file)
	for index, package in enumerate(data):
		repoName = data[index]["packageName"]
		repoName.encode("utf-8")
		npmUrl = "https://registry.npmjs.org/" + repoName

		#Issues with "/" in name of packages replacing "/" with "_"
		for i, c in enumerate(repoName):
			if(c == '/'):
				repoName = repoName[:i-1] + "_" + repoName[i+1:]
		#Download the JSON from registry
		downloadCommand = "wget -q -O " + repoName + ".json " + npmUrl
		os.system(downloadCommand)

		jsonRepoName = repoName + ".json"
		with open(jsonRepoName, "r") as read_file:
			dataNpm = json.load(read_file)
			print "Populating -> ", repoName
			latestVersion = dataNpm["dist-tags"]["latest"]
			latestVersion.encode("utf-8")
			if "repository" not in dataNpm:
				print "No Url Github Repository found"
				noUrlCount = noUrlCount + 1
			else:	
				githubUrl = dataNpm["versions"][latestVersion]["repository"]["url"]
				print githubUrl
				data[index]["githubUrl"] = githubUrl
			
			#Remove downloaded JSONs
			removeCommand = "rm " + repoName + ".json"
			os.system(removeCommand)
			print "Completed -> ", repoName

with io.open('../assets/npmGithubUrl.json', 'w', encoding='utf-8') as f:
  f.write(json.dumps(data, ensure_ascii=False))

print "Number of Repos without Github Url", noUrlCount
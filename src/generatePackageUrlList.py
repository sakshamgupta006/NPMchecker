import json
import pprint

def createPackageJson():
	packageListHash = []
	inputFile = open('../assets/most-dependent-upon.md', 'r') 
	for line in inputFile: 
		nameStart = '['
		nameEnd = ']'
		npmUrlStart = '('
		npmUrlEnd = ')'
		lineStr = str(line)
		name = (lineStr.split(nameStart))[1].split(nameEnd)[0]
		npmUrl = (lineStr.split(npmUrlStart))[1].split(npmUrlEnd)[0]
		packageObj = {}
		packageObj["packageName"] = name
		packageObj["npmUrl"] = npmUrl
		packageListHash.append(packageObj)
	
	pprint.pprint(packageListHash)

createPackageJson()

from os import listdir
from os.path import isfile, join
import json

mypath = "../latest/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
total_old_packages = 0
total_new_packages = 0
total_packages = 0
for index, currentFile in enumerate(onlyfiles):
    currentJson  = mypath + currentFile
    with open(currentJson, "r") as read_package:
        total_packages += 1
        dataPackage = json.load(read_package)
        if "latest" in dataPackage:
            total_new_packages += dataPackage["latest"]["count"]
        if "old" in dataPackage:
            total_old_packages += dataPackage["old"]["count"]
print ("Total New: ", total_new_packages)
print ("Total Old: ", total_old_packages)
print ("Total Packages ", total_packages)

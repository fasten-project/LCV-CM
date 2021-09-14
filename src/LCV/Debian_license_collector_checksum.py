import sys
#from LCVlib.testlistsGithubAPI import GitHubURLList
#from LCVlib.testlistsJSONfiles import JSONPathList
#from LCVlib.verify import retrieveOutboundLicense, CheckOutboundLicense
#from LCVlib.verify import RetrieveInboundLicenses, Compare, CompareFlag
from dotenv import load_dotenv
from os import environ, path
import os
import requests
import json
import time
import sys
import pandas as pd
import numpy as np
import re
import fileinput
from LCVlib.SPDXIdMapping import StaticMappingList,IsAnSPDX,StaticMapping,DynamicMapping,IsInAliases,ConvertToSPDX
from LCVlib.VerboseLicenseParsing import RemoveParenthesisAndSpecialChars
from LCVlib.CommonLists import *
from LCVlib.DebianAPILib import *
#from LCVlib.verify import CSV_to_dataframeOSADL

'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''


# create a for that loops from START_LINE up to END_LINE

# Load .env file
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
# Load parametrs from .env file
startLine = environ.get('START_LINE')
endLine = environ.get('END_LINE')

print("Scanning from line:"+str(startLine))
print("to line:"+str(endLine))


startLine = int(startLine) + 1
endLine = int(endLine) + 1

"""
https://sources.debian.org/copyright/api/sha256/?checksum=1be7080d72e6b566df3e236ce2c55efdfbbb8fa1c972d825e5b672ff8773be1a
&package=0ad&suite=bullseye
"""

for i in range(int(startLine),int(endLine)):
    p = int(i)
    print(p)
    packageName = GetPackageName(p)
    packageName = packageName.strip()
    debianVersion = "bullseye"
    parent_dir = "collectingDebianLicenses"
    dir = "collectingDebianLicenses/"+packageName
    parent_dirChecksum = "collectingDebianLicensesChecksum/"+packageName
    #If the directory doesn't exist, create it and scan the package.
    if not os.path.isdir(parent_dirChecksum):
        print("creating directory")
        CreateDirectory(parent_dirChecksum,packageName)
    else:
        print(parent_dirChecksum+" already exists")
    #this loop creates the first layer of files and directories
    for (root,dirs,files) in os.walk(dir, topdown=True):
        for directory in dirs:
            print(root)
            print(dirs)
            print(".. looping through directory ..: " +root+"/"+directory)
            rootCheckusm = root.replace("collectingDebianLicenses","collectingDebianLicensesChecksum/")
            if not os.path.isdir(rootCheckusm+"/"+directory):
                print("creating directory:"+rootCheckusm+"/"+directory)
                CreateDirectory("",rootCheckusm+"/"+directory)
            for file in os.listdir(root+"/"+directory):
                if "_dir.json" in file or "_pkg.json" in file:
                    print(file+" is not json of a file" )
                    continue
                if ".json" in file:
                    path = dir
                    pathChecksum = root.replace("collectingDebianLicenses","collectingDebianLicensesChecksum")
                    pathChecksum = pathChecksum+"/"+directory+"/"+file
                    print(pathChecksum)
                    if not os.path.isfile(pathChecksum):
                        path = path.replace("collectingDebianLicenses/"+packageName+"/","")
                        print("Running ScanJsonDirChecksum upon :"+root+"/"+directory+"/"+file)
                        ScanJsonDirChecksum(root+"/"+directory,packageName,file)
                        time.sleep(1.2)
        for file in files:
            print(".. looping through files .. " +file)
            if "_dir.json" in file or "_pkg.json" in file:
                print("this is not json of a file" )
                continue
            if ".json" in file:
                path = dir
                pathChecksum = root.replace("collectingDebianLicenses","collectingDebianLicensesChecksum")
                pathChecksum = pathChecksum+"/"+directory+"/"+file
                print(pathChecksum)
                if not os.path.isfile(pathChecksum):
                    path = path.replace("collectingDebianLicenses/"+packageName+"/","")
                    print("Running ScanJsonDirChecksum upon :"+root+"/"+directory+"/"+file)
                    ScanJsonDirChecksum(root+"/"+directory,packageName,file)
                    time.sleep(1.2)

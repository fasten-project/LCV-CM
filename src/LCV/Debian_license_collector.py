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

packageName = "davfs2"
packageVersion = "latest"
parent_dir = "collectingDebianLicenses/"
dir = "collectingDebianLicenses/davfs2/"
#dir = "/home/michelescarlato/gitrepo/LCV-CM-Fasten/src/LCV/collectingDebianLicenses/davfs2/"


CreateDirectory(parent_dir,packageName)
RetrievePackageFilesAndDirectory(packageName)
#parse davfs2_pkg.json
ScanJsonDir(dir,packageName+"_pkg.json")


#this loop create the first layer of files and directories
for (root,dirs,files) in os.walk(dir, topdown=True):
    if not os.listdir(root):
        print("This is an empty dir")
        root = root.replace("collectingDebianLicenses/"+packageName+"/","")
        RetrieveDirectoryInfoNotRecursive(root)
    print ("root: ")
    print (root)
    print (len(root+"/"))
    print ("dirs: ")
    print (dirs)
    print ("files: ")
    print (files)
    print ('--------------------------------')
    for file in files:
        print(".. looping through files .. " +file)
        if "_dir.json" in file:
            path = dir
            path = path.replace("collectingDebianLicenses/"+packageName+"/","")
            print(path)
            ScanJsonDir(root+"/",file)
            time.sleep(1)
    for directory in dirs:
        print(".. looping through directory ..: " +root+directory)
        for file in os.listdir(root+"/"+directory):
        #if len(root+"/"+directory) == 0:
            print("This is an empty dir")
            RetrieveDirectoryInfo(root+"/"+directory)
        else:
            for file in os.listdir(root+"/"+directory):
                print("Inside "+directory+" there is :"+file)

#this loop create the second layer of files and directories
for (root,dirs,files) in os.walk(dir, topdown=True):
    print("######### Second for ##############")
    if not os.listdir(root):
        print("This is an empty dir")
        root = root.replace("collectingDebianLicenses/"+packageName+"/","")
        RetrieveDirectoryInfoNotRecursive(root)
    print ("root: ")
    print (root)
    #print (len(root+"/"))
    print ("dirs: ")
    print (dirs)
    print ("files: ")
    print (files)
    print ('--------------------------------')
    for directory in dirs:
        print(".. looping through directory ..: " +root+directory)
        #if len(root+"/"+directory) == 0:
        if not os.listdir(root+"/"+directory):
            print("This is an empty dir")
            RetrieveDirectoryInfo(root+"/"+directory)
            time.sleep(1)
        for file in os.listdir(root+"/"+directory):
            print("Inside "+directory+" there is :"+file)
            if "_dir.json" in file:
                path = dir
                path = path.replace("collectingDebianLicenses/"+packageName+"/","")
                print(path)
                ScanJsonDir(root,file)
                time.sleep(1)

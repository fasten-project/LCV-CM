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

def RetrievePackageFilesAndDirectory(packageName):
    #Example: GET https://Debian.org/Debian/standalone/1.0.1/json
    response = requests.get("https://sources.debian.org/api/src/"+packageName+"/latest/")
    time.sleep(2)
    if response.status_code == 200:
        jsonResponse=response.json()
        with open('collectingDebianLicenses/'+packageName+'/'+packageName+'.json', 'w', encoding='utf-8') as f:
            json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
        return jsonResponse
    else:
        jsonResponse = "404"
        #output= jsonResponse+", 404 - page not found"
        #print(output)
        return jsonResponse

def CreateDirectory(root,directory):
    #parent_dir = "./collectingDebianLicenses/"+packageName
    path = os.path.join(root, directory)
    try:
        os.makedirs(path, exist_ok = True)
        print("Directory '%s' created successfully" % directory)
        print(path)
        return path
    except OSError as error:
        print("Directory '%s' can not be created" % directory)


def RetrieveFilesInfo(path):
    fileName = path
    path = packageName+"/"+packageVersion+"/"+path
    print(path)
    response = requests.get("https://sources.debian.org/api/src/"+path+"/")
    #response = requests.get("https://sources.debian.org/api/src/"+packageName+"/"+packageVersion+"/"+fileName+"/")
    time.sleep(2)
    if response.status_code == 200:
        jsonResponse=response.json()
        #print(jsonResponse)
        with open('collectingDebianLicenses/'+packageName+'/'+fileName+'.json', 'w', encoding='utf-8') as f:
            json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
        return jsonResponse
        '''
        fname = 'collectingDebianLicenses/'+packageName+fileName+'_dir.json'
        if os.path.isfile(fname):
            with open('collectingDebianLicenses/'+path+'.json', 'w', encoding='utf-8') as f:
                json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
                return jsonResponse
        '''
    else:
        jsonResponse = "404"
        output = jsonResponse+", 404 - page not found"
        #print(output)
        #appendToFile(output)
        return output

def RetrieveDirectoryInfo(path):
    directory = path
    path = packageName+"/"+packageVersion+"/"+path
    response = requests.get("https://sources.debian.org/api/src/"+path+"/")
    time.sleep(2)
    if response.status_code == 200:
        jsonResponse=response.json()
        fname = 'collectingDebianLicenses/'+packageName+directory+directory+'_dir.json'
        if os.path.isfile(fname):
            with open(fname, 'w', encoding='utf-8') as f:
                json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
                return jsonResponse
    else:
        jsonResponse = "404"
        output = jsonResponse+", 404 - page not found"
        #print(output)
        #appendToFile(output)
        return output

#data = RetrievePackageFilesAndDirectory(packageName)

def ScanJson(root,jsonFile):
    fname = root+"/"+jsonFile
    #print(os.path.isfile(fname))
    if os.path.isfile(fname):
        with open(root+"/"+jsonFile, 'r') as f:
            print("Opening file")
            print(jsonFile)
            dict = json.load(f)
            #print(dict)
            subDict = dict["content"]
            #print(subDict)
        for item in subDict:
            if item["type"] == "directory":
                directory = item["name"]
                #print("Creating directory")
                path=CreateDirectory(root,directory)
                path = path.replace("collectingDebianLicenses/"+packageName+"","")
                print (path)
                RetrieveDirectoryInfo(path)
                #print(directory)
            if item["type"] == "file":
                fileName = item["name"]
                print(fileName)
                print(root)
                path = root+fileName
                path = path.replace("collectingDebianLicenses/"+packageName+"/","")
                print(path)
                RetrieveFilesInfo(path)
                #data = RetrieveFilesCheckusm(directory,fileName)
                #print("Checking for checksum:")
                #print(data)



CreateDirectory(parent_dir,packageName)
RetrievePackageFilesAndDirectory(packageName)

'''
packageNameJson = packageName+".json"
ScanJson(parent_dir,packageNameJson)
'''
for (root,dirs,files) in os.walk(dir, topdown=True):
        print (root)
        print (dirs)
        print (files)
        print ('--------------------------------')
        for file in files:
            if ".json" in file:
                print (file+" is a json file")
                #pathToJsonFile = root+"/"+file
                #print(pathToJsonFile)
                ScanJson(root, file)
                time.sleep(3)


'''
files = os.listdir(dir)
for f in files:
    print(f)
    if "_dir" in f:
        print(f+" contains directory information")
'''

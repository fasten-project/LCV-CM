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

def RetrievePackageFilesAndDirectory(packageName):
    print("https://sources.debian.org/api/src/"+packageName+"/latest/")
    response = requests.get("https://sources.debian.org/api/src/"+packageName+"/latest/")
    time.sleep(2)
    if response.status_code == 200:
        jsonResponse=response.json()
        with open('collectingDebianLicenses/'+packageName+'/'+packageName+'_pkg.json', 'w', encoding='utf-8') as f:
            print("writing file")
            json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
        return jsonResponse
    else:
        jsonResponse = "404"
        return jsonResponse

def CreateDirectory(root,directory):
    path = os.path.join(root, directory)
    try:
        os.makedirs(path, exist_ok = True)
        print("Directory '%s' created successfully" % directory)
        #print(path)
        return path
    except OSError as error:
        print("Directory '%s' can not be created" % directory)


def RetrieveFilesInfo(path):
    fileName = path
    path = packageName+"/"+packageVersion+"/"+path
    #print(path)
    print("https://sources.debian.org/api/src/"+path+"/")
    response = requests.get("https://sources.debian.org/api/src/"+path+"/")
    #response = requests.get("https://sources.debian.org/api/src/"+packageName+"/"+packageVersion+"/"+fileName+"/")
    time.sleep(1)
    if response.status_code == 200:
        jsonResponse=response.json()
        #print(jsonResponse)
        with open('collectingDebianLicenses/'+packageName+'/'+fileName+'.json', 'w', encoding='utf-8') as f:
            json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
        return jsonResponse
    else:
        jsonResponse = "404"
        output = jsonResponse+", 404 - page not found"
        #print(output)
        #appendToFile(output)
        return output

def RetrieveDirectoryInfo(path):
    #print("Inside of DirectoryInfo")
    directory = path
    path = packageName+"/"+packageVersion+"/"+path
    print("https://sources.debian.org/api/src/"+path+"/")
    response = requests.get("https://sources.debian.org/api/src/"+path+"/")
    time.sleep(1)
    if response.status_code == 200:
        print("status code 200")
        jsonResponse=response.json()
        #print(jsonResponse)
        fname = 'collectingDebianLicenses/'+packageName+"/"+directory+"/"+directory+'_dir.json'
        # this control is required to scan nested directories
        #if os.path.isfile(fname):
        if os.path.isfile(fname):
            with open(fname, 'w', encoding='utf-8') as f:
                json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
                return jsonResponse
    else:
        jsonResponse = "404"
        output = jsonResponse+", 404 - page not found"
        return output

def RetrieveDirectoryInfoNotRecursive(path):
    #print("Inside of DirectoryInfo")
    directory = path
    fileName = path
    fileName = fileName.replace("/"," ")
    fileNameList = fileName.split()
    #print(fileNameList)
    fileName = fileNameList[-1]
    #print(fileName)
    path = packageName+"/"+packageVersion+"/"+path
    print("https://sources.debian.org/api/src/"+path+"/")
    response = requests.get("https://sources.debian.org/api/src/"+path+"/")
    time.sleep(1)
    if response.status_code == 200:
        print("status code 200")
        jsonResponse=response.json()
        #print(jsonResponse)
        fname = 'collectingDebianLicenses/'+packageName+"/"+directory+"/"+fileName+'_dir.json'
        # this control is required to scan nested directories
        #if os.path.isfile(fname):
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
            return jsonResponse
    else:
        jsonResponse = "404"
        output = jsonResponse+", 404 - page not found"
        return output




def ScanJsonDir(root,jsonFile):
    fname = root+jsonFile
    print("Fname is:")
    print(fname)
    #print(os.path.isfile(fname))
    #print("inside dir.json and pkg.json loop")
    if os.path.isfile(fname):
        with open(root+"/"+jsonFile, 'r') as f:
            print("Opening file")
            print(jsonFile)
            dict = json.load(f)
            subDict = dict["content"]
        for item in subDict:
            if item["type"] == "directory":
                directory = item["name"]
                path = CreateDirectory(root,directory)
                path = path.replace("collectingDebianLicenses/"+packageName+"/","")
                #print (path)
                RetrieveDirectoryInfoNotRecursive(path)
            if item["type"] == "file":
                fileName = item["name"]
                #print(fileName)
                #print(root)
                path = root+fileName
                path = path.replace("collectingDebianLicenses/"+packageName+"/","")
                print(path)
                RetrieveFilesInfo(path)

def ScanJsonFile(root,jsonFile):
    print("this is from inside ScanJsonFile")
    return

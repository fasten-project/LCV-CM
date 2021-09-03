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



def RetrievePackageFilesAndDirectory(packageName):
    #Example: GET https://Debian.org/Debian/standalone/1.0.1/json
    response = requests.get("https://sources.debian.org/api/src/"+packageName+"/latest/")
    time.sleep(2)
    if response.status_code == 200:
        jsonResponse=response.json()
        with open('collectingDebianLicenses/'+packageName+'.json', 'w', encoding='utf-8') as f:
            json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
        return jsonResponse

    else:
        jsonResponse = "404"
        #output= jsonResponse+", 404 - page not found"
        #print(output)
        return jsonResponse

def CreateDirectory(directory):
    parent_dir = "./collectingDebianLicenses/"+packageName
    path = os.path.join(parent_dir, directory)
    try:
        os.makedirs(path, exist_ok = True)
        print("Directory '%s' created successfully" % directory)
    except OSError as error:
        print("Directory '%s' can not be created" % directory)


def RetrieveFilesCheckusm(directory,fileName):
    if directory is not None:
        response = requests.get("https://sources.debian.org/api/src/"+directory+"/"+fileName+"/")
        time.sleep(2)
        if response.status_code == 200:
            jsonResponse=response.json()
            with open('collectingDebianLicenses/'+directory+'/'+packageName+'.json', 'w', encoding='utf-8') as f:
                json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
                return jsonResponse
        else:
            jsonResponse = "404"
            output = jsonResponse+", 404 - page not found"
            #print(output)
            #appendToFile(output)
            return output
    else:
        response = requests.get("https://sources.debian.org/api/src/"+fileName+"/")
        time.sleep(2)
        if response.status_code == 200:
            jsonResponse=response.json()
            with open('collectingDebianLicenses/'+packageName+'.json', 'w', encoding='utf-8') as f:
                json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
                return jsonResponse    

data = RetrievePackageFilesAndDirectory(packageName)

with open('collectingDebianLicenses/'+packageName+'.json', 'r') as f:
    print("Opening file")
    dict = json.load(f)
    subDict = dict["content"]
    print(subDict)

for item in subDict:
    if item["type"] == "directory":
        directory = item["name"]
        print("CreateDirectory")
        CreateDirectory(directory)
        print(directory)
    if item["type"] == "file":
        fileName = item["name"]
        #data = RetrieveFilesCheckusm(directory,fileName)
        print("Checking for checksum:")
        print(data)

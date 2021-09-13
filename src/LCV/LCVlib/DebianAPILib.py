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

#packageName = "0ad"
packageVersion = "latest"
debianVersion = "bullseye"

def GetPackageName(line_number):
    fp = open("clean_whole_debian_packages_list.txt")
    for i, packageName in enumerate(fp):
        if i == line_number:
            fp.close()
            print(packageName)
            return packageName



def RetrievePackageFilesAndDirectory(packageName):
    print("https://sources.debian.org/api/src/"+packageName+"/latest/")
    response = requests.get("https://sources.debian.org/api/src/"+packageName+"/latest/", timeout=None)
    time.sleep(1.2)
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
    print("Inside create directory:")
    print("root :"+root)
    print("directory :"+directory)
    print("path :"+path)
    try:
        os.makedirs(path, exist_ok = True)
        print("Directory '%s' created successfully" % directory)
        #print(path)
        return path
    except OSError as error:
        print("Directory '%s' can not be created" % directory)

def RetrieveFilesInfo(packageName,path):
    fileName = path
    path = packageName+"/"+packageVersion+"/"+path
    #print(path)
    print("https://sources.debian.org/api/src/"+path+"/")
    response = requests.get("https://sources.debian.org/api/src/"+path+"/", timeout=None)
    time.sleep(1.2)
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

def RetrieveDirectoryInfo(packageName,path):
    #print("Inside of DirectoryInfo")
    directory = path
    path = packageName+"/"+packageVersion+"/"+path
    print("https://sources.debian.org/api/src/"+path+"/")
    response = requests.get("https://sources.debian.org/api/src/"+path+"/", timeout=None)
    time.sleep(1.2)
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

def RetrieveDirectoryInfoNotRecursive(packageName,path):
    #print("Inside of DirectoryInfo")
    directory = path
    print(directory)
    fileName = path
    fileName = fileName.replace("/"," ")
    fileNameList = fileName.split()
    #print(fileNameList)
    fileName = fileNameList[-1]
    #print(fileName)
    path = packageName+"/"+packageVersion+"/"+path
    print("https://sources.debian.org/api/src/"+path+"/")
    response = requests.get("https://sources.debian.org/api/src/"+path+"/", timeout=None)
    time.sleep(1.2)
    if response.status_code == 200:
        print("status code 200")
        jsonResponse=response.json()
        #print(jsonResponse)
        fname = 'collectingDebianLicenses/'+packageName+"/"+directory+"/"+fileName+'_dir.json'
        # this control is required to scan nested directories
        #if os.path.isfile(fname):
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
            root = 'collectingDebianLicenses/'+packageName+'/'+directory
            jsonFile = fileName+'_dir.json'
            print(root)
            print(jsonFile)
        ScanJsonDir(packageName,root,jsonFile)
        return jsonResponse
    else:
        jsonResponse = "404"
        output = jsonResponse+", 404 - page not found"
        return output

def ScanJsonDir(packageName,root,jsonFile):
    fname = root+"/"+jsonFile
    print("Fname is:")
    print(fname)
    #print(os.path.isfile(fname))
    #print("inside dir.json and pkg.json loop")
    if os.path.isfile(fname):
        with open(fname, 'r') as f:
            print("Opening file")
            print(fname)
            #print(f)
            currentPath = os.getcwd()
            print("Current Path:")
            print(currentPath)
            #if fname == None or f == '':
            #    print('I got a null or empty string value for data in a file')
            dict = json.load(f)
            print(dict)
            subDict = dict["content"]
        for item in subDict:
            if item["type"] == "directory":
                directory = item["name"]
                path = root + "/" + directory
                print("This is the path of a directory found in the :"+ path)
                print(path)
                if "//" in path:
                    path = path.replace("//","/")
                    print("ModPath:")
                    print(path)
                if not os.path.isdir(path):
                    path = CreateDirectory(root,directory)
                    path = path.replace("collectingDebianLicenses/"+packageName+"/","")
                    print (path)
                    print ("Inside of type directory in ScanJsonDir")
                    time.sleep(1.2)
                    RetrieveDirectoryInfoNotRecursive(packageName,path)
                else:
                    print("Directory already exist")
            if item["type"] == "file":
                fileName = item["name"]
                path = root+"/"+fileName
                print("This is the path of a file found in the :"+ path)
                print(path)
                if "//" in path:
                    path = path.replace("//","/")
                    print("ModPath:")
                    print(path)
                if not os.path.isfile(path+".json"):
                    #print(fileName)
                    #print(root)
                    path = path.replace("collectingDebianLicenses/"+packageName+"/","")
                    print("Path generated inside of ScanJsonDir for FILE type")
                    print(path)
                    RetrieveFilesInfo(packageName,path)
                else:
                    print("File already exist")
# currently not used
def ScanJsonFile(packageName,root,jsonFile):
    print("this is from inside ScanJsonFile")
    return

def ScanJsonDirChecksum(packageName,root,jsonFile):
    fname = root+"/"+jsonFile
    directory = root.replace("collectingDebianLicenses/"+packageName+"/","")
    print("Fname is:")
    print(fname)
    if os.path.isfile(fname):
        with open(fname, 'r') as f:
            print("Opening file")
            print(fname)
            dict = json.load(f)
            print(dict)
            #subDict = dict["content"]
            checksum = dict["checksum"]

        response = requests.get("https://sources.debian.org/copyright/api/sha256/?checksum="+checksum+"&package="+packageName+"&suite="+debianVersion, timeout=None)
        time.sleep(1.2)
        if response.status_code == 200:
            print("status code 200")
            jsonResponse=response.json()
            #print(jsonResponse)
            fname = 'collectingDebianLicensesChecksum/'+packageName+"/"+directory+"/"+jsonFile
            if "//" in fname:
                fname = fname.replace("//","/")
                print("ModFname:")
                print(fname)
            # this control is required to scan nested directories
            #if os.path.isfile(fname):
            if not os.path.isdir('collectingDebianLicensesChecksum/'+packageName+"/"+directory+"/"):
                print("creating directory")
                CreateDirectory("collectingDebianLicensesChecksum",packageName+"/"+directory)
            with open(fname, 'w', encoding='utf-8') as f:
                json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
                #root = 'collectingDebianLicensesChecksum/'+packageName+'/'+directory
                #jsonFile = fileName+'_dir.json'
                #print(root)
                #print(jsonFile)
            #ScanJsonDirChecksum(packageName,root,jsonFile)
            return jsonResponse
        else:
            jsonResponse = "404"
            output = jsonResponse+", 404 - page not found"
            return output


# currently not used

def RetrieveChecksum(path):
    return checksum

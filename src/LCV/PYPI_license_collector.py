import sys
#from LCVlib.testlistsGithubAPI import GitHubURLList
#from LCVlib.testlistsJSONfiles import JSONPathList
#from LCVlib.verify import retrieveOutboundLicense, CheckOutboundLicense
#from LCVlib.verify import RetrieveInboundLicenses, Compare, CompareFlag
from dotenv import load_dotenv
from os import environ, path
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

# Load .env file
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
# Load parametrs from .env file
startLine = environ.get('START_LINE')
endLine = environ.get('END_LINE')

print("Scanning from line:"+startLine)
print("to line:"+endLine)


def RetrievePypiLicenseInformationPackage(packageName):
    #Example: GET https://pypi.org/pypi/standalone/1.0.1/json
    response = requests.get("https://pypi.org/pypi/"+packageName+"/json")
    if response.status_code == 200:
        jsonResponse=response.json()
        license=(jsonResponse["info"]["license"])
        return license
    else:
        license = "404"
        output=packageName+", 404 - page not found"
        print(output)
        appendToFile(output)
        return license


def RetrievePypiLicenseInformationPackageVersion(packageName,packageVersion):
    #Example: GET https://pypi.org/pypi/standalone/1.0.1/json
    response = requests.get("https://pypi.org/pypi/"+packageName+"/"+packageVersion+"/json")
    jsonResponse=response.json()
    license=(jsonResponse["info"]["license"])
    return license

def APICallConvertToSPDX(license):
    #response = requests.get("https://lima.ewi.tudelft.nl/lcv/ConvertToSPDX?VerboseLicense="+license)
    response = requests.get("http://0.0.0.0:3251/ConvertToSPDX?VerboseLicense="+license)
    jsonResponse=response.json()
    #print(jsonResponse)
    return jsonResponse

def APICallIsAnSPDX(license):
    #response = requests.get("https://lima.ewi.tudelft.nl/lcv/IsAnSPDX?SPDXid="+license)
    response = requests.get("http://0.0.0.0:3251/IsAnSPDX?SPDXid="+license)
    jsonResponse=response.json()
    #print(jsonResponse)
    return jsonResponse

def appendToFile(license):
    with open("collectingPypiLicenses/output/whole-pypi-package-list-ConvertToSPDX"+str(startLine)+"-"+str(endLine)+".txt", "a+") as file_object:
    #with open("collectingPypiLicenses/output/Re-factoring-testing.txt", "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(license)


with open('whole_pypi_package_list.txt') as f:
    packages=[]
    packages_unstripped = f.readlines()[int(startLine):int(endLine)]
    print(packages_unstripped)
    for package in packages_unstripped:
        packages.append(package.rstrip())
    print(packages)

for package in packages:
    output = None
    license = RetrievePypiLicenseInformationPackage(package)
    if license is not None and not license == "" and not license == "404":
        if "same as" in license:
            strippedName = []
            strippedName = license.split()
            for name in strippedName:
                if name is "same" or name is "as":
                    strippedName.remove(name)
            licenseName =''.join(strippedName)
            licenseName = licenseName.lower()
            license = RetrievePypiLicenseInformationPackage(licenseName)
        # trying to catch long license declarations
        # TODO append some special output to indicate that here the margin of error is higher
        if "www." in license:
            TryingConversion = ConvertToSPDX(license)
            print("XXXXXXXXXXXXXXXX")
            print(TryingConversion)
            license=TryingConversion
        for char in list_of_parenthesis:
            if char in license:
                license = RemoveParenthesisAndSpecialChars(license)
        possibleSPDX = license
        IsSPDX = APICallIsAnSPDX(license)
        if IsSPDX:
            IsSPDX = "Pypi provided an SPDX id."
        else:
            if "+" in license:
                licenseMod=license.replace("+", "%2B")
                possibleSPDX = APICallConvertToSPDX(licenseMod)
            else:
                possibleSPDX = APICallConvertToSPDX(license)
            if possibleSPDX is not None:
                IsSPDX = APICallIsAnSPDX(possibleSPDX)
                if IsSPDX:
                    IsSPDX = "Converted."
                if not IsSPDX:
                    IsSPDX = "NOT Converted."
        line_number = 0
        # add line number
        with open('whole_pypi_package_list.txt', 'r') as g:
            for line in g:
                line_number += 1
                if re.search(rf"\b(?=\w){package}\b(?!\w)", line, re.IGNORECASE):
                    output=str(line_number)+" "+package+",\n"+str(license)+",\n"+str(possibleSPDX)+",\n"+str(IsSPDX)
                    print(output)
        if output is None:
                output=package+",\n"+str(license)+",\n"+str(possibleSPDX)+",\n"+str(IsSPDX)
                print(output)
        appendToFile(output)
    if license is None or license == "":
        output=package+", detected pypi license: None"
        print(output)
        appendToFile(output)
    if license == "404":
        print("404 - page not found")
    time.sleep(5)


def ScanningRequirementsTXT():
    # for requirements.txt, where package versions are specified.
    with open('input/requirements.txt') as f:
        packages = [line.rstrip() for line in f]
        print(packages)

    for package in packages:
        if ('==' in package):
            packages = package.replace('==', ' ')
        if ('>=' in package):
            packages = package.replace('>=', ' ')
        if ('=>' in package):
            packages = package.replace('=>', ' ')
        strings = packages.split()
        packageName=strings[0]
        packageVersion=strings[1]
        license = RetrievePypiLicenseInformationPackageVersion(packageName,packageVersion)
        if license is not None and not license == "":
            possibleSPDX = license
            IsSPDX = APICallIsAnSPDX(license)
            if IsSPDX:
                IsSPDX = "Pypi provided an SPDX id."
            else:
                if "+" in license:
                    licenseMod=license.replace("+", "%2B")
                    possibleSPDX = APICallConvertToSPDX(licenseMod)
                else:
                    possibleSPDX = APICallConvertToSPDX(license)
                IsSPDX = APICallIsAnSPDX(possibleSPDX)
                if IsSPDX:
                    IsSPDX = "Converted."
                if not IsSPDX:
                    IsSPDX = "NOT Converted."
            output=packageName+"=="+packageVersion+",\n"+str(license)+",\n"+str(possibleSPDX)+",\n"+str(IsSPDX)
            print(output)
            appendToFile(output)
        else:
            output=packageName+"=="+packageVersion+", detected pypi license: None"
            print(output)
            appendToFile(output)
        time.sleep(5)

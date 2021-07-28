import sys
#from LCVlib.testlistsGithubAPI import GitHubURLList
#from LCVlib.testlistsJSONfiles import JSONPathList
#from LCVlib.verify import retrieveOutboundLicense, CheckOutboundLicense
#from LCVlib.verify import RetrieveInboundLicenses, Compare, CompareFlag
import requests
import json
import time
import sys
import pandas as pd
import numpy as np
import re
#from LCVlib.SPDXIdMapping import StaticMappingList,IsAnSPDX,StaticMapping,DynamicMapping,IsInAliases,ConvertToSPDX
#from LCVlib.verify import CSV_to_dataframeOSADL

'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''



def RetrievePypiLicenseInformation(packageName,packageVersion):
    #GET https://pypi.org/pypi/standalone/json
    response = requests.get("https://pypi.org/pypi/"+packageName+"/"+packageVersion+"/json")
    jsonResponse=response.json()
    #data = json.loads(jsonResponse)
    license=(jsonResponse["info"]["license"])
    return license

def appendToFile(license):
    with open("pypi-license-list.txt", "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(license)


with open('requirements.txt') as f:
    packages = [line.rstrip() for line in f]
    print(packages)

for package in packages:
    if '==' in package:
        packages = package.replace('==', ' ')
        strings = packages.split()
        packageName=strings[0]
        packageVersion=strings[1]
        license = RetrievePypiLicenseInformation(packageName,packageVersion)
        print(license)
        appendToFile(license)

'''
license = RetrievePypiLicenseInformation("standalone","1.0.1")
print(license)
appendToFile(license)
'''

'''
for packageName in packages:
    license = RetrievePypiLicenseInformation("standalone","1.0")
    appendToFile(license)
'''

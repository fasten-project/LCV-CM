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

import json

packageNameList = []
# some JSON:
fname = "collectingDebianLicenses/whole_debian_packages_list.json"
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
    #print(dict)
    subDict = dict["packages"]
    for item in subDict:
        packageName = item["name"]
        packageNameList.append(packageName)

fnameList = "collectingDebianLicenses/clean_whole_debian_packages_list.json"

with open(fnameList, 'w', encoding='utf-8') as f:
    #json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
    for item in packageNameList:
        f.write("%s\n" % item)






# parse x:
#y = json.loads(x)

# the result is a Python dictionary:
#print(y["age"])

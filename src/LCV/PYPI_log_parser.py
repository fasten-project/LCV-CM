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
import glob
import os
from LCVlib.SPDXIdMapping import StaticMappingList,IsAnSPDX,StaticMapping,DynamicMapping,IsInAliases,ConvertToSPDX
from LCVlib.pypi_license_retrieval import *

#from LCVlib.verify import CSV_to_dataframeOSADL

'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''


excluded_not_converted= ["ASL","GPL","LGPL","AGPL", "AFL","ASF", "BOLA", "GNU", "Creative Commons", "Copyleft",
"Private","UNKNOWN","BSD","Apache","MPL","LPPL","None", "other", "CC-BY-NC-SA", "Python", "Marsyas", "Mozilla",
"License", "LICENCE","LICENSE","LICENSE.txt","Dual License", "Proprietary", "todo", "TODO",
"Artistic","ZPL","ASK FOR PERMISSIONS","NA","nothing","opensource","OSL","public","Public Domain", "Private","Proprietary License",
"PSL", "All Rights Reserved", "WPI", "CeCILL","OSI","LUMS", "UCSD", "EUPL" , "EULA", "CDDL",
"commercial","undefined","CC-BY-SA", "Free", "Freeware", "EPL", "RPL", "TBD", "Custom", "COPYING", "COPYRIGHT", "SSPL"
]

already_fixed= ["GNU v3", "MIT;", "CC0","APL", "CeCILL-B", "zlib",
"CC BY-SA 3.0", "CC by 4.0", "EUPL v1.2 or later", "BEERWARE",
"cc-by-sa-4.0", "beer", "ISCL", "ISC-style", "SSPL"
"Attribution-NonCommercial-ShareAlike 4.0 International",
"Attribution-ShareAlike 4.0 International CC BY-SA 4.0", "CC BY-SA 4.0",
"Attribution-NonCommercial-NoDerivatives 4.0 International CC BY-NC-ND 4.0",
"CC BY-NC-SA 4.0", "CCSA-4.0", "CC BY-NC 4.0","IBM", "CC4.0-BY-NC-SA",
"wxWindows","CC BY-NC-ND 4.0","ICS", "MIT/Expat", "MIT/X",
"https://creativecommons.org/publicdomain/zero/1.0/",
"SIL OFL 1.1", "NIST", "D-FSL", "Unlisence",
]



FinalList = []
for filename in glob.glob('collectingPypiLicenses/output/whole*.txt'):
   with open(os.path.join(os.getcwd(), filename), 'r') as f:
       lines = f.readlines()
       for index, line in enumerate(lines):  # enumerate the list and loop through it
        if "NOT Converted" in line:  # check if the current line has your substring
            #print("inside not converted")
            LineList= (lines[max(0,index-3):index])
            for i in range(0, len(LineList)):
                for line in LineList:
                    if ",\n" in line:
                        LineList.remove(line)
                        modLine=line.replace(",\n","")
                        LineList.append(modLine)
            output = LineList[0]+ " " + LineList[1]
            FinalList.append(output)

            if "same as" in output:
                #print("inside same as")
                FinalList.remove(output)
                #print(LineList[1])
                license = LineList[1]
                package = LineList[0]
                strippedName = []
                strippedName = license.split()
                for i in range(0, len(strippedName)):
                    for name in strippedName:
                        if name == "same":# if name == "as":
                            strippedName.remove(name)
                        if name == "as":
                            strippedName.remove(name)
                #print(strippedName)
                licenseName =''.join(strippedName)
                licenseName = licenseName.lower()
                #print(licenseName)
                license = RetrievePypiLicenseInformationPackage(licenseName)
                time.sleep(1)
                output = "output:"+package+ " " + license
                #print(output)
                FinalList.append(output)
            for excluded in excluded_not_converted:
                if excluded.lower() in output.lower():
                    if output in FinalList:
                        FinalList.remove(output)
            for fixed in already_fixed:
                if fixed.lower() in output.lower():
                    if output in FinalList:
                        FinalList.remove(output)
for output in FinalList:
    print(output+'\n')
    #print()

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
#from LCVlib.verify import CSV_to_dataframeOSADL

'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''


excluded_not_converted= ["GPL","LGPL","AGPL", "AFL", "GNU", "Creative Commons",
"Private","UNKNOWN","BSD","Apache","MPL","None", "CC-BY-NC-SA", "Python", "Marsyas",
"License", "LICENCE","LICENSE","LICENSE.txt","Dual License", "Proprietary", "todo","TODO",
"Artistic","ZPL","ASK FOR PERMISSIONS","Public Domain", "Private","Proprietary License", "PSL", "All Rights Reserved", "WPI"]

already_fixed= ["GNU v3", "MIT;", "CC0","APL", "CeCILL-B", "zlib", "CC BY-SA 3.0", "CC by 4.0", "EUPL v1.2 or later", "BEERWARE", "cc-by-sa-4.0" ]
FinalList = []
for filename in glob.glob('collectingPypiLicenses/output/*.txt'):
   with open(os.path.join(os.getcwd(), filename), 'r') as f:
       lines = f.readlines()
       for index, line in enumerate(lines):  # enumerate the list and loop through it
        if "NOT Converted" in line:  # check if the current line has your substring
            LineList= (lines[max(0,index-3):index])
            for i in range(0, len(LineList)):
                for line in LineList:
                    if ",\n" in line:
                        LineList.remove(line)
                        modLine=line.replace(",\n","")
                        LineList.append(modLine)
            output = LineList[0]+ " " + LineList[1]
            FinalList.append(output)
            for excluded in excluded_not_converted:
                if excluded.lower() in output.lower():
                    #print (excluded.lower())
                    #print (output.lower())
                    if output in FinalList:
                        FinalList.remove(output)
            for fixed in already_fixed:
                if fixed.lower() in output.lower():
                    #print (excluded.lower())
                    #print (output.lower())
                    if output in FinalList:
                        FinalList.remove(output)
for output in FinalList:
    print(output+'\n')
    #print()

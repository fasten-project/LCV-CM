import sys
from LCVlib.testlistsGithubAPI import GitHubURLList
from LCVlib.testlistsJSONfiles import JSONPathList
# from LCVlib.verify import retrieveOutboundLicense, CheckOutboundLicense
# from LCVlib.verify import RetrieveInboundLicenses, Compare, CompareFlag
import requests
import json
import time
import sys
import pandas as pd
import numpy as np
import re
import os
from LCVlib.SPDXIdMapping import StaticMappingList, IsAnSPDX, StaticMapping, DynamicMapping, IsInAliases, ConvertToSPDX
from LCVlib.CheckAliasAndSPDXId import *
from LCVlib.CommonLists import *
from LCVlib.VerboseLicenseParsing import *
from LCVlib.verify import CSV_to_dataframeOSADL


'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''

currentPath = os.getcwd()
print("Current Path:")
print(currentPath)

"""

license = "GPL99"
OutboundLicense = "Diesel95"
#dict.fromkeys([message, status, inbound, outbound])
keys = ["message","status","inbound","outbound"]
dictOutput = dict.fromkeys(keys, None)
print(dictOutput)


output = license+" is not compatible with " + \
    OutboundLicense+" as an outbound license"

dictOutput['message'] = output
dictOutput['status'] = "not compatible"
dictOutput['inbound'] = license
dictOutput['outbound'] = OutboundLicense

print(dictOutput)
#print(dictOutput)
"""

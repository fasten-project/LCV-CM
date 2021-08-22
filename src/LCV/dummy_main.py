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
from LCVlib.SPDXIdMapping import StaticMappingList, IsAnSPDX, StaticMapping, DynamicMapping, IsInAliases, ConvertToSPDX
from LCVlib.verify import CSV_to_dataframeOSADL

'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''
'''
verbose_license = 'MIT license, ! '

endingSpecChars= '[,!.?](?:\s+)?$'
while(re.findall(endingSpecChars, verbose_license)):
    verbose_license = re.sub(endingSpecChars,'', verbose_license)
    print(verbose_license)
'''
# test the ConvertToSPDX method

licenseSPDX = ConvertToSPDX("MIT license, ! ")
print(licenseSPDX)


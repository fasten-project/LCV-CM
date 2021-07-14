import sys
from LCVlib.testlistsGithubAPI import GitHubURLList
from LCVlib.testlistsJSONfiles import JSONPathList
#from LCVlib.verify import retrieveOutboundLicense, CheckOutboundLicense
#from LCVlib.verify import RetrieveInboundLicenses, Compare, CompareFlag
import requests
import json
import time
import sys
import pandas as pd
import numpy as np
import re
from LCVlib.SPDXIdMapping import StaticMappingList,IsAnSPDX,StaticMapping,DynamicMapping,IsInAliases,ConvertToSPDX
from LCVlib.verify import CSV_to_dataframeOSADL

'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''

df = CSV_to_dataframeOSADL("../../csv/OSADL.csv")
supported_licenses_OSADL = list(df.index)
#print(supported_licenses_OSADL)


license_list = ['AGPL 3.0 not aliases or later','AGPL 3.0 only','AGPL only not alias  3.0','The Apache Software License, Version 2.0', 'Apache License, Version 1.0','AGPL 3.0 or later','GPL 3.0 only','MIT Licensed']
#license_list = ['AGPL 3.0 not aliases or later']
#license_list = ['AGPL 3.0 not aliases']
#re approach

# Currently the algorithm is not able to reason like: "General Public License = GPL"
# Artistic is artistic-1.0-perl, try to catch it!
# BSD contains the Clause word after the version number - which is not including .0 or .1
# bzip versions are in the format 1.0.5 or 1.0.6.
# still you are not catching classpath with this logic
# MIT CMU will be hardly recognized
# MPL no copyleft cannot be recognized with this method
# MS-PL (Microsoft Public License) and MS-RL (Microsoft Reciprocal License) cannot be recognized
# Unicode DFS 2015 and 2016 currently cannot be re-composed.
# zlib-acknowledgement can be matched only with hyphen in the middle, inasmuch zlib is written equally.

licenses = ["AFL","AGPL","Apache","Artistic","BSD","BSL","bzip2","CC0","CDDL","CPL","curl","EFL","EPL","EUPL","FTL","GPL","HPND","IBM","ICU","IJG","IPL","ISC",
"LGPL","Libpng","libtiff","MirOS","MIT","CMU","MPL","MS","NBPL","NTP","OpenSSL","OSL","Python","Qhull","RPL","SunPro","Unicode","UPL","WTFPL","X11","XFree86","Zlib","zlib-acknowledgement"]
versions = ["1.0","1.0.5","1.0.6","1.1","1.5","2.0","2.1","3.0","3.1"]

# To do: excluding the "," from parsing - currently it remains attached to the License, word e.g.

for verbose_license in license_list:
    print("################")
    SPDX_id=ConvertToSPDX(verbose_license)
    print("Resulting SPDX:")
    print(SPDX_id)



#debugging
'''
if IsAnAlias:
    print("Supposed License is an Alias: "+supposedLicense)
else:
    print("Supposed License is NOT an Alias: "+supposedLicense)
if IsSPDX:
    print("Supposed License SPDX is an SPDX: "+supposedLicenseSPDX)
else:
    print("Supposed License SPDX is NOT an SPDX: "+supposedLicenseSPDX)
'''

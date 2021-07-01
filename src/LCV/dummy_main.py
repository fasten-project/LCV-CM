import sys
from LCVlib.testlistsGithubAPI import GitHubURLList
from LCVlib.testlistsJSONfiles import JSONPathList
from LCVlib.verify import retrieveOutboundLicense, CheckOutboundLicense
from LCVlib.verify import RetrieveInboundLicenses, Compare, CompareFlag
import requests
import json
import time
import sys
import pandas as pd
import numpy as np
'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''

CSVfilePath = "/home/michelescarlato/gitrepo/LCV-CM-Fasten/LCV-CM/csv/OSADL_transposed.csv"

# Outbound
column_names_list = ['MIT']
column_names_list.insert(0, 'License')
df = pd.read_csv(CSVfilePath, usecols=column_names_list)
print(df)
License = "Pippo"


Column_array = df.to_numpy()

#df.loc[:, 'License']
print(Column_array)
if (License in Column_array):
    print("License is in the Matrix")
else:
    print("License is not in the Matrix")
#df[~df.License.isin(License)]

#print(df)
#df.iloc[-1, -1] = "License"
#print(df)

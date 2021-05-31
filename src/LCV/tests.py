from LCVlib.verify import retrieveOutboundLicense, RetrieveInboundLicenses, Compare
from LCVlib.verify import runtimer, CheckOutboundLicense, CompareFlag
from LCVlib.testlistsJSONfiles import JSONPathList
from LCVlib.testlistsGithubAPI import GitHubURLList
'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''

JSONPath = JSONPathList()
GitHubURL = GitHubURLList()
index = 0
# With CM.csv tests 1 (because of Public Domain), 7, 9, 24 and 30 not functioning
t = 10
empty = ""
orLater = "or-later"
# while url in GitHubURL:
while index < len(GitHubURL):
    URL = GitHubURL[index]
    JSON = JSONPath[index]
    testnumber = index + 1
    print("#################")
    print("##Running test number "+str(testnumber))
    print("#################")
    OutboundLicense = retrieveOutboundLicense(URL)
    OutboundLicense = CheckOutboundLicense(OutboundLicense)
    if OutboundLicense is not None:
        InboundLicenses = RetrieveInboundLicenses(JSON)
        verificationFlag = CompareFlag(InboundLicenses, OutboundLicense)
        if (verificationFlag is True):
            print("The set of inbound licenses is compatible with the outbound one")
            verificationList = Compare(InboundLicenses, OutboundLicense)
            print("Print verification list:")
            print(verificationList)
        if (verificationFlag is False):
            print("Compatibility issues found .... generating logs")
            verificationList = Compare(InboundLicenses, OutboundLicense)
            print("Print verification list:")
            print(verificationList)
        if (verificationFlag == "DUC"):
            print("Compatibility depending on the use case .... generating logs")
            verificationList = Compare(InboundLicenses, OutboundLicense)
            print("Print verification list:")
            print(verificationList)
        # verificationList = Compare(InboundLicenses, OutboundLicense)
        # print("Print verification list:")
        # print(verificationList)
    runtimer(t)
    index += 1
    print(index)

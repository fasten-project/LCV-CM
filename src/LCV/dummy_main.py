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

license = RetrievePypiLicenseInformation("standalone","1.0.1")
print(license)
appendToFile(license)
'''
for packageName in packages:
    license = RetrievePypiLicenseInformation("standalone","1.0")
    appendToFile(license)
'''


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

MappedKeywords=["general","library"]
if ("general" in MappedKeywords) and (("affero" and "lesser" and "library") not in MappedKeywords):# and "lesser" not in MappedKeywords:
    licenseName = "GPL"
    print(licenseName)
else:
    licenseName = "AGPL"
    print(licenseName)


def DetectWithAcronyms(verbose_license):
    licenseVersion = None
    licenseName = None
    supposedLicense = None
    only=False
    orLater=False

    list_of_words = verbose_license.split()
    for word in list_of_words:
        if word in licenses:
            licenseName=word
        if word in versions:
            licenseVersion=word
            if licenseVersion == "1" or "2" or "3" or "4" or "5":
                licenseVersion=str(float(licenseVersion))
        if word.lower() == "later":
            orLater=True
        if word.lower() == "only":
            only=True
    if licenseName is not None and licenseVersion is None:
        supposedLicense = licenseName
    if not orLater and not only:
        if licenseName and licenseVersion is not None:
            supposedLicense = licenseName+" "+licenseVersion
    if orLater:
        if licenseName and licenseVersion is not None:
            supposedLicense = licenseName+" "+licenseVersion+" or later"
    if only:
        if licenseName and licenseVersion is not None:
            supposedLicense = licenseName+" "+licenseVersion+" only"
    if supposedLicense is not None:
        return supposedLicense
    else:
        return verbose_license

def DetectWithKeywords(verbose_license):
    # probably you could declare globally this variable - inasmuch it is also used by the DetectWithAcronyms() function
    licenseVersion = None
    licenseName = None
    DynamicMappingKeywordsList=[
        "2010","academic","affero","attribution","berkeley","bsd","bzip","cmu","commons","creative","commons","database","distribution","eclipse","epl","eupl","european",
        "exception","general","ibm","later","lesser","libpng","license","miros","mozilla","mpl,""ntp","only","openssl","patent","python","png","power","powerpc","public","permissive","qhull",
        "reciprocal","software","tiff","uc","universal","upl","zlib","zero"]

    MappedKeywords=[]
    #check with keywords
    for word in list_of_words:
        if word.lower() in DynamicMappingKeywordsList:
            append.MappedKeywords(word.lower())
        if word in versions:
            licenseVersion=word
            if licenseVersion == "1" or "2" or "3" or "4" or "5":
                licenseVersion=str(float(licenseVersion))

    #If there are keywords matched
    if len(MappedKeywords):
        if "academic" in MappedKeywords:
            licenseName = "AFL"
        # this check should consider also 2-1.0.5 ..
        if "bzip" or "2010" in MappedKeywords:
            licenseName = "bzip2-1.0.6"
            return licenseName
        if "distribution" in MappedKeywords:
            licenseName = "CDDL"
        if "powerpc" or "power" in MappedKeywords:
            licenseName = "IBM-pibs"
        if "tiff" in MappedKeywords:
            licenseName = "libtiff"
        if "miros" in MappedKeywords:
            licenseName = "MirOS"
            return licenseName
        if "cmu" in MappedKeywords:
            licenseName = "MIT-CMU"
            return licenseName
        if "bsd" and "patent" in MappedKeywords:
            licenseName = "BSD-2-Clause-Patent"
            return licenseName
        if "bsd" and "uc" in MappedKeywords:
            licenseName = "BSD-4-Clause-UC"
            return licenseName
        if "bsd" and "database" in MappedKeywords:
            licenseName = "Sleepycat"
            return licenseName
        if "ibm" and "public" in MappedKeywords:
            licenseName = "IPL-1.0"
            return licenseName
        if "libpng" in MappedKeywords and not "zlib" in MappedKeywords and licenseVersion is None:
            licenseName = "Libpng"
        if "libpng" in MappedKeywords and licenseVersion == "2.0":
            licenseName = "libpng-2.0"
            return licenseName
        if "eclipse" in MappedKeywords and licenseVersion == "1.0":
            licenseName = "EPL-1.0"
            return licenseName
        if "eclipse" in MappedKeywords and licenseVersion == "2.0":
            licenseName = "EPL-2.0"
            return licenseName
        if "libpng" in MappedKeywords and "zlib" in MappedKeywords:
            licenseName = "Zlib"

        if "european" in MappedKeywords and licenseVersion == "1.0":
            licenseName = "EUPL-1.0"
            return licenseName
        if "european" in MappedKeywords and licenseVersion == "1.1":
            licenseName = "EUPL-1.1"
            return licenseName
        if "european" in MappedKeywords and licenseVersion == "1.2":
            licenseName = "EUPL-1.2"
            return licenseName
        if "mozilla" in MappedKeywords and licenseVersion == "1.0":
            licenseName = "MPL-1.0"
            return licenseName
        if "mozilla" in MappedKeywords and licenseVersion == "1.1":
            licenseName = "MPL-1.1"
            return licenseName
        if "mozilla" in MappedKeywords and licenseVersion == "2.0" and exception not in MappedKeywords:
            licenseName = "MPL-2.0"
            return licenseName
        if "mozilla" in MappedKeywords and exception in MappedKeywords and licenseVersion == "2.0":
            licenseName = "MPL-2.0-no-copyleft-exception"
            return licenseName
        if "sleepycat" in MappedKeywords:
            licenseName = "Sleepycat"
            return licenseName
        if "ntp" and "attribution" in MappedKeywords:
            licenseName = "NTP-0"
            return licenseName
        if "ntp" in MappedKeywords and attribution not in MappedKeywords:
            licenseName = "NTP"
            return licenseName
        if "upl" in MappedKeywords:
            licenseName = "UPL-1.0"
            return licenseName
        if "universal" and "permissive" in MappedKeywords:
            licenseName = "UPL-1.0"
            return licenseName
        if "creative" and "commons" and "universal" in MappedKeywords:
            licenseName = "CC0-1.0"
            return licenseName
        if "creative" and "zero" in MappedKeywords:
            licenseName = "CC0-1.0"
            return licenseName
        if "python" and "software" in MappedKeywords:
            licenseName = "PSF-2.0"
            return licenseName
        if "python" in MappedKeywords and licenseVersion == "2.0" and software not in MappedKeywords:
            licenseName = "Python-2.0"
            return licenseName
        if "openssl" in MappedKeywords:
            licenseName = "OpenSSL"
            return licenseName
        if "qhull" in MappedKeywords:
            licenseName = "Qhull"
            return licenseName
        if "reciprocal" and "public" and "license" in MappedKeywords and licenseVersion == "1.5":
            licenseName = "RPL-1.5"
            return licenseName
        if "reciprocal" and "public" and "license" in MappedKeywords and licenseVersion == "1.1":
            licenseName = "RPL-1.1"
            return licenseName

        if "affero" in MappedKeywords:
            licenseName = "AGPL"
        if "lesser" in MappedKeywords:
            licenseName = "LGPL"
        if "general" in MappedKeywords and "affero" not in MappedKeywords and "lesser" not in MappedKeywords:
            licenseName = "GPL"

    if licenseName is not None and licenseVersion is None:
        supposedLicense = licenseName
    # check if is or later or only, if not, just assign license name and license version
    if not orLater and not only:
        if licenseName and licenseVersion is not None:
            supposedLicense = licenseName+" "+licenseVersion
    if orLater:
        if licenseName and licenseVersion is not None:
            supposedLicense = licenseName+" "+licenseVersion+" or later"
    if only:
        if licenseName and licenseVersion is not None:
            supposedLicense = licenseName+" "+licenseVersion+" only"
    if supposedLicense is not None:
        return supposedLicense
    else:
        return verbose_license


'''
'''
def DynamicMappingRefactoring(verbose_license):
    detectedWithAcronymsLicense = DetectWithAcronyms(verbose_license)
    IsSPDX = IsAnSPDX(detectedWithAcronymsLicense)
    if IsSPDX :
        print(detectedWithAcronymsLicense+" is an SPDX-id")
        return detectedWithAcronymsLicense
    IsAnAlias = IsInAliases(detectedWithAcronymsLicense)
    if IsAnAlias:
        print(detectedWithAcronymsLicense)
        detectedWithAcronymsLicense = StaticMapping(detectedWithAcronymsLicense)
        IsSPDX = IsAnSPDX(detectedWithAcronymsLicense)
        if IsSPDX :
            print(detectedWithAcronymsLicense+" is an SPDX-id")
            return detectedWithAcronymsLicense

    detectedWithKeywordsLicense = DetectWithKeywords(verbose_license)
    IsSPDX = IsAnSPDX(detectedWithKeywordsLicense)
    if IsSPDX :
      print(detectedWithKeywordsLicense+" is an SPDX-id")
      return detectedWithKeywordsLicense
    IsAnAlias = IsInAliases(detectedWithKeywordsLicense)
    if IsAnAlias:
      print(detectedWithKeywordsLicense)
      detectedWithKeywordsLicense = StaticMapping(detectedWithKeywordsLicense)
      IsSPDX = IsAnSPDX(detectedWithKeywordsLicense)
      if IsSPDX :
          print(detectedWithKeywordsLicense+" is an SPDX-id")
          return detectedWithKeywordsLicense
    if not IsAnAlias:
        return verbose_license

    if supposedLicense is not None:
        print("Supposed license:")
        print(supposedLicense)
        IsAnAlias = IsInAliases(supposedLicense)
    #if supposedLicenseSPDX is not None:
        IsSPDX = IsAnSPDX(supposedLicense)
    # the next three if could be simply the else of the last if - currently debugging
    if IsAnAlias: #and IsSPDX:
        return supposedLicense#,supposedLicenseSPDX
    #if IsAnAlias and not IsSPDX:
        #return supposedLicense,supposedLicenseSPDX
    if IsSPDX:
        return supposedLicense
    if not IsAnAlias:# and IsSPDX:
        return verbose_license#supposedLicense,supposedLicenseSPDX
    #if not IsAnAlias and not IsSPDX:
        #print("enters here")
        #return verbose_license,supposedLicenseSPDX
    '''

'''
for verbose_license in license_list:
    print("################")
    SPDX_id=DynamicMappingRefactoring(verbose_license)
    print("Resulting SPDX:")
    print(SPDX_id)
'''

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
from LCVlib.CheckAliasAndSPDXId import *
from LCVlib.CommonLists import *
from LCVlib.VerboseLicenseParsing import *
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
'''
def ConvertToSPDXTesting(verbose_license):
    print("Testing DynamicMapping upon:")
    print(verbose_license)
    #license_names = []
    license_name = DynamicMappingTesting(verbose_license)
    print("Dynamic mapping result: ")
    print(license_name)
    IsAnAlias = IsInAliases(license_name)
    if IsAnAlias:
        #print(license_name)
        license_mapped = StaticMapping(license_name)
        IsSPDX = IsAnSPDX(license_mapped)
        if IsSPDX:
            print(license_mapped+" is an SPDX-id")
            return license_mapped
    else:
        return license_name

def DynamicMappingTesting(verbose_license):
    verbose_license = RemoveParenthesisAndSpecialChars(verbose_license)
    detectedWithKeywordsLicense = DetectWithKeywords(verbose_license)
    detectedWithKeywordsLicense = MappingResultCheck(detectedWithKeywordsLicense)
    #IsSPDX = IsAnSPDX(detectedWithKeywordsLicense)
    if IsAnSPDX(detectedWithKeywordsLicense):
        return detectedWithKeywordsLicense
    else:
        return verbose_license

def MappingResultCheck(detectedLicense):
    IsSPDX = IsAnSPDX(detectedLicense)
    if IsSPDX:
        print(detectedLicense+" is an SPDX-id")
        return detectedLicense
    IsAnAlias = IsInAliases(detectedLicense)
    if IsAnAlias:
        print(detectedLicense)
        detectedLicense = StaticMapping(
            detectedLicense)
        IsSPDX = IsAnSPDX(detectedLicense)
        if IsSPDX:
            print(detectedLicense+" is an SPDX-id")
            return detectedLicense
    #if not IsAnAlias:
    return detectedLicense


def DetectWithKeywords(verbose_license):
    # probably you could declare globally these variables - inasmuch it is also used by the DetectWithAcronyms() function
    licenseVersion = None
    licenseName = None
    supposedLicense = None
    orLater = False
    only = False
    MappedKeywords = list()
    list_of_words = verbose_license.split()

    for word in list_of_words:
        #probably here I can use a list of separators, e.g. "-", ">=" ..
        # and check if elements of the list are contained in word,
        # then replace them, split and append.
        if not IsAnSPDX(word) and '-' in word:
            if word in list_of_words:
                list_of_words.remove(word)
            words = word.replace('-', ' ')
            strings = words.split()
            for string in strings:
                list_of_words.append(string)
            continue
        if '>=' in word:
            orLater = True
            list_of_words.remove(word)
            words = word.replace('>=', ' ')
            strings = words.split()
            for string in strings:
                list_of_words.append(string)
        startWithV = bool(re.match('v', word, re.I))
        if not startWithV:
            list_of_words = detectV(list_of_words,word)
        if startWithV:
            word = ConformVersionNumber(word)
            if word.isdigit():
                licenseVersion=word
        endWithPlus = word.endswith('+')
        if endWithPlus:
            orLater=True
            if word in list_of_words:
                list_of_words.remove(word)
            word=word.replace('+', '')
            list_of_words.append(word)
    #check with keywords
    for word in list_of_words:
        # check case insensitive starting with v words, to catch vX.X cases.
        if bool(re.match('v', word, re.I)):
            word = ConformVersionNumber(word)
        # check cases like GPL2, Apache1, LGPL3 cases.

        if bool(re.match('[Aa-zZ]+[0-9].?[0-9]?', word, re.I)):
            #if word not in versions:
            #if not word.isdigit():
            print(word)
            word = SeparateLicenseNameAndVersionNumber(word)
            strings = word.split()
            for string in strings:
                list_of_words.append(string)

        if word.lower() in literalVersions:
            licenseVersion = (str(NumberDict[word.lower()]))
        if word.lower() in DynamicMappingKeywordsList:
            MappedKeywords.append(word.lower())
        if word in versions:
            licenseVersion = str(word)
        if word.lower() in LicenseLetterVersion:
            MappedKeywords.append(word.lower())
        if licenseVersion is not None:
            if licenseVersion == "1" or "2" or "3" or "4" or "5":
                licenseVersion = str(float(licenseVersion))
                MappedKeywords.append(licenseVersion)
            else:
                MappedKeywords.append(licenseVersion)
                print(MappedKeywords)
    # remove duplicates from the MappedKeywords
    MappedKeywords = list(set(MappedKeywords))
    print("Mapped Keywords:")
    print(MappedKeywords)
    #If there are keywords matched --> this can be a dictionary and nested dictionary in case of double match
    if len(MappedKeywords):
        if "later" in MappedKeywords:
            orLater = True
        if "only" in MappedKeywords:
            only = True
        print("found this")
        print([v for k,v in DynamicMappingKeywordsDict.items() if k in MappedKeywords])
        #[k for k, v in champ_dict.items() if v in champ_ids]
        
        if "bsd" in MappedKeywords:
            if "open" and "mpi" in MappedKeywords:
                licenseName = "BSD-3-Clause-Open-MPI"
                return licenseName
            if "simplified" in MappedKeywords:
                licenseName = "BSD-2-Clause"
                return licenseName
            if "patent" in MappedKeywords:
                licenseName = "BSD-2-Clause-Patent"
                return licenseName
            if "uc" in MappedKeywords:
                licenseName = "BSD-4-Clause-UC"
                return licenseName
            if "database" in MappedKeywords:
                licenseName = "Sleepycat"
                return licenseName
            if "shortened" in MappedKeywords:
                licenseName = "BSD-4-Clause-Shortened"
                return licenseName
            if "nuclear" in MappedKeywords:
                if "2014" in MappedKeywords:
                    licenseName = "BSD-3-Clause-No-Nuclear-License-2014"
                    return licenseName
                if "warranty" in MappedKeywords:
                    licenseName = "BSD-3-Clause-No-Nuclear-Warranty"
                    return licenseName
                licenseName = "BSD-3-Clause-No-Nuclear-License"
                return licenseName
            if "modification" in MappedKeywords:
                licenseName = "BSD-3-Clause-Modification"
                return licenseName
            if "national" in MappedKeywords:
                licenseName = "BSD-3-Clause-LBNL"
                return licenseName
            if "clear" in MappedKeywords:
                licenseName = "BSD-3-Clause-Clear"
                return licenseName
            if "attribution" in MappedKeywords:
                licenseName = "BSD-3-Clause-Attribution"
                return licenseName
            if "military" in MappedKeywords:
                licenseName = "BSD-3-Clause-No-Military-License"
                return licenseName
            if "views" in MappedKeywords:
                licenseName = "BSD-2-Clause-Views"
                return licenseName
            if "patent" in MappedKeywords:
                licenseName = "BSD-2-Clause-Patent"
                return licenseName
            if licenseVersion == "2.0":
                licenseName = "BSD-2-Clause"
                return licenseName
            if licenseVersion == "3.0" or "new" in MappedKeywords:
                licenseName = "BSD-3-Clause"
                return licenseName
        
    print("License Version")
    print(licenseVersion)
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
licenseSPDX = ConvertToSPDX("CeCILL-C")
print(licenseSPDX)

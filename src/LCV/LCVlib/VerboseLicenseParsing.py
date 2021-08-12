#!/usr/bin/python
# import urllib.request
import requests
import json
import time
import sys
import pandas as pd
import numpy as np
import re
import csv
from LCVlib.CommonLists import *

'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''

def detectV(list_of_words,word):
    if len(list_of_words) < 10:
        if 'v' in word or 'V' in word:
            words = re.compile("v", re.IGNORECASE)
            words = words.sub(" ", word)
            strings = words.split()
            # check if after 'v' there is a digit
            word2 = strings[1]
            if word2[0].isdigit():
                # run the conversion
                word = ConformLicenseNameAndVersionNumber(word)
                words = word.split()
                # append all the splitted words to the matching list
                for word in words:
                    list_of_words.append(word)
    return list_of_words


def DetectWithAcronyms(verbose_license):
    licenseVersion = None
    licenseName = None
    supposedLicense = None
    only = False
    orLater = False

    list_of_words = verbose_license.split()
    for word in list_of_words:
        startWithV = bool(re.match('v', word, re.I))
        print(startWithV)
        if not startWithV:
            #print(word)
            #print(word)
            list_of_words = detectV(list_of_words,word)
        if startWithV:
            print(word)
            word = ConformVersionNumber(word)
            if word.isdigit():
                licenseVersion=word

        #list_of_words = detectV(list_of_words,word)
        '''
        if len(list_of_words) < 10:
            if 'v' in word:
                print(len(list_of_words))
                words = word.replace('v', ' ')
                strings = words.split()
                # check if after 'v' there is a digit
                word2 = strings[1]
                if word2[0].isdigit():
                    word = ConformLicenseNameAndVersionNumber(word)
                    words = word.split()
                    # append all the splitted words to the matching list
                    for word in words:
                        list_of_words.append(word)
        '''
        if word in licenses:
            licenseName = word
        if word in versions:
            licenseVersion = word
            if licenseVersion == "1" or "2" or "3" or "4" or "5":
                licenseVersion = str(float(licenseVersion))
        if word.lower() == "later":
            orLater = True
        if word.lower() == "only":
            only = True
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


def ConformVersionNumber(licenseVersion):
    pattern = 'v[+-]?([0-9]*[.])?[0-9]+'
    matchObj = re.match(pattern, licenseVersion,re.IGNORECASE)
    if matchObj:
        licenseVersionV = re.compile("v", re.IGNORECASE)
        licenseVersionV = licenseVersionV.sub("", licenseVersion)
        licenseVersion = licenseVersionV
        #licenseVersion = licenseVersion.replace('v', '')
        print(licenseVersion)
        return licenseVersion
    else:
        return licenseVersion

def ConformLicenseNameAndVersionNumber(licenseName):
    pattern = '\w+v[0-9]?.?[0-9]'
    matchObj = re.match(pattern, licenseName,re.IGNORECASE)
    if matchObj:
        licenseNameV = re.compile("v", re.IGNORECASE)
        licenseNameV = licenseNameV.sub("", licenseName)
        licenseName = licenseNameV
        #licenseName.replace('v', ' ')
        #licenseName = licenseName.replace('V', ' ')
        return licenseName
    else:
        return licenseName


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
        if '-' in word:
            list_of_words.remove(word)
            words = word.replace('-', ' ')
            strings = words.split()
            for string in strings:
                list_of_words.append(string)
            print("list_of_words")
            print(list_of_words)
        #@me it should be considered also the "V" case
        startWithV = bool(re.match('v', word, re.I))
        #print(startWithV)
        if not startWithV:
            #print(word)
            #print(word)
            list_of_words = detectV(list_of_words,word)
        '''
        if len(list_of_words) < 10:
            if 'v' in word:
                words = word.replace('v', ' ')
                strings = words.split()
                # check if after 'v' there is a digit
                word2 = strings[1]
                if word2[0].isdigit():
                    word = ConformLicenseNameAndVersionNumber(word)
                    words = word.split()
                    # append all the splitted words to the matching list
                    for word in words:
                        list_of_words.append(word)
        '''
    #check with keywords
    for word in list_of_words:
        # check case insesitive starting with v words, to catch vX.X cases.
        if bool(re.match('v', word, re.I)):
            word = ConformVersionNumber(word)

        if word.lower() in literalVersions:
            licenseVersion = (str(NumberDict[word.lower()]))
        if "(" or ")" or "[" or "]" in word:
            word = re.sub(r"[()]", "", word)
            word = re.sub(r"[\[\]]", "", word)
        #print("After running ConformVersionNumber: "+word)
        if word.lower() in DynamicMappingKeywordsList:
            MappedKeywords.append(word.lower())
        if word in versions:
            licenseVersion = str(word)
        if licenseVersion is not None:
            if licenseVersion == "1" or "2" or "3" or "4" or "5":
                licenseVersion = str(float(licenseVersion))
                MappedKeywords.append(licenseVersion)
            else:
                MappedKeywords.append(licenseVersion)
                print(MappedKeywords)
    MappedKeywords = list(set(MappedKeywords))
    print("Mapped Keywords:")
    print(MappedKeywords)
    #If there are keywords matched --> this can be a dictionary and nested dictionary in case of double match
    if len(MappedKeywords):
        if "later" in MappedKeywords:
            orLater = True
        if "only" in MappedKeywords:
            only = True
        if "academic" in MappedKeywords:
            licenseName = "AFL"
        # this check should consider also 2-1.0.5 ..
        if "bzip" in MappedKeywords or "2010" in MappedKeywords:
            licenseName = "bzip2-1.0.6"
            return licenseName
        if "distribution" in MappedKeywords:
            licenseName = "CDDL"
        if "powerpc" in MappedKeywords or "power" in MappedKeywords:
            licenseName = "IBM-pibs"
        if "tiff" in MappedKeywords:
            licenseName = "libtiff"
        if "miros" in MappedKeywords:
            licenseName = "MirOS"
            return licenseName
        if "mit" in MappedKeywords:
            licenseName = "MIT"
            return licenseName
        if "cmu" in MappedKeywords:
            licenseName = "MIT-CMU"
            return licenseName
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

        if "classpath" in MappedKeywords or "cpe" in MappedKeywords:
            licenseName = "GPL-2.0-with-classpath-exception"
            return licenseName
        if "expat" in MappedKeywords:
            licenseName = "MIT"
            return licenseName
        if "ibm" in MappedKeywords and "public" in MappedKeywords:
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
        if "mozilla" in MappedKeywords and licenseVersion == "2.0" and "exception" not in MappedKeywords:
            licenseName = "MPL-2.0"
            return licenseName
        if "mozilla" in MappedKeywords and "exception" in MappedKeywords and licenseVersion == "2.0":
            licenseName = "MPL-2.0-no-copyleft-exception"
            return licenseName
        if "sleepycat" in MappedKeywords:
            licenseName = "Sleepycat"
            return licenseName
        if "ntp" in MappedKeywords and "attribution" in MappedKeywords:
            licenseName = "NTP-0"
            return licenseName
        if "ntp" in MappedKeywords and "attribution" not in MappedKeywords:
            licenseName = "NTP"
            return licenseName
        if "upl" in MappedKeywords:
            licenseName = "UPL-1.0"
            return licenseName
        if "universal" in MappedKeywords and "permissive" in MappedKeywords:
            licenseName = "UPL-1.0"
            return licenseName
        if "creative" in MappedKeywords and "commons" in MappedKeywords and "universal" in MappedKeywords:
            licenseName = "CC0-1.0"
            return licenseName
        if "creative" in MappedKeywords and "zero" in MappedKeywords in MappedKeywords:
            licenseName = "CC0-1.0"
            return licenseName
        if "python" in MappedKeywords and "software" in MappedKeywords:
            licenseName = "PSF-2.0"
            return licenseName
        if "psf" in MappedKeywords or "psfl" in MappedKeywords:
            licenseName = "PSF-2.0"
            return licenseName
        if "python" in MappedKeywords and licenseVersion == "2.0" and "software" not in MappedKeywords:
            licenseName = "Python-2.0"
            return licenseName
        if "openssl" in MappedKeywords:
            licenseName = "OpenSSL"
            return licenseName
        if "qhull" in MappedKeywords:
            licenseName = "Qhull"
            return licenseName
        if "reciprocal" in MappedKeywords and "public" in MappedKeywords and "license" in MappedKeywords:
            if licenseVersion == "1.5":
                licenseName = "RPL-1.5"
                return licenseName
            if licenseVersion == "1.1":
                licenseName = "RPL-1.1"
                return licenseName
        if "affero" in MappedKeywords:
            licenseName = "AGPL"
        if "library" in MappedKeywords or "lesser" in MappedKeywords or "lgpl" in MappedKeywords:
            licenseName = "LGPL"
            if orLater:
                if licenseVersion == "2.0" or licenseVersion == "2.1" or licenseVersion == "3.0":
                    licenseName = "LGPL-"+licenseVersion+"-or-later"
                    return licenseName
            if licenseVersion == "2.0" or licenseVersion == "2.1" or licenseVersion == "3.0":
                licenseName = "LGPL-"+licenseVersion+"-only"
                return licenseName
        if "gpl" in MappedKeywords:
            licenseName = "GPL"
            if orLater:
                if licenseVersion == "2.0" or licenseVersion == "2.1" or licenseVersion == "3.0":
                    licenseName = "GPL-"+licenseVersion+"-or-later"
                    return licenseName
            if licenseVersion == "2.0" or licenseVersion == "2.1" or licenseVersion == "3.0":
                licenseName = "GPL-"+licenseVersion+"-only"
                return licenseName

        if ("general" in MappedKeywords) and "affero" not in MappedKeywords and "lesser" not in MappedKeywords and "library" not in MappedKeywords:# and "lesser" not in MappedKeywords:
            licenseName = "GPL"
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

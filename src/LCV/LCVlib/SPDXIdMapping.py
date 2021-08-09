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

'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''

licenses = ["AFL", "AGPL", "Apache", "Artistic", "BSD", "BSL", "bzip2", "CC0", "CDDL", "CPE", "CPL", "curl", "EFL", "EPL", "EUPL", "FTL", "GPL", "HPND", "IBM", "ICU", "IJG", "IPL", "ISC",
            "LGPL", "Libpng", "libtiff", "MirOS", "MIT", "CMU", "MPL", "MS", "NBPL", "NTP", "OpenSSL", "OSL", "Python", "Qhull", "RPL", "SunPro", "Unicode", "UPL", "WTFPL", "X11", "XFree86", "Zlib", "zlib-acknowledgement"]
versions = ["1.0", "1.0.5", "1.0.6", "1.1", "1.2", "1.5",
            "2.0", "2.1", "3.0", "3.1", "1", "2", "3", "4", "5"]


def CSV_to_dataframe(CSVfilePath, column_names_list):
    """
    Import a CSV and transform it into a pandas dataframe selecting only the useful columns from the Compatibility Matrix
    """
    df = pd.read_csv(CSVfilePath, usecols=column_names_list)
    return df


def IsInAliases(single_verbose_license):
    CSVfilePath = "../../csv/spdx-id.csv"
    IsInAliases = False
    with open(CSVfilePath, 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            # if the username shall be on column 3 (-> index 2)
            if single_verbose_license == row[0]:
                print(single_verbose_license+" is a recognized Alias")
                IsInAliases = True
                return IsInAliases
        if not IsInAliases:
            print(single_verbose_license+" is a not recognized Alias")
            return IsInAliases


def StaticMapping(single_verbose_license):
    CSVfilePath = "../../csv/spdx-id.csv"
    column_names_list = ['Scancode', 'SPDX-ID']
    df = CSV_to_dataframe(CSVfilePath, column_names_list)
    df = df.set_index('Scancode')
    single_verbose_license_SPDX_id = df.loc[single_verbose_license]['SPDX-ID']
    if single_verbose_license_SPDX_id is not np.nan:
        return single_verbose_license_SPDX_id
    #probably this else shouldn't exist
    else:
        return single_verbose_license


def IsAnSPDX(license_name):
    IsSPDX = False
    with open('../../csv/SPDX_license_name.csv', 'rt') as f:
        reader = csv.reader(f)
        for row in reader:
            for field in row:
                if field == license_name:
                    IsSPDX = True
                    return IsSPDX


def ConvertToSPDX(verbose_license):
    IsAnAlias = False
    IsAnAlias = IsInAliases(verbose_license)
    # if verbose license is within aliases - run static mapping
    if IsAnAlias:
        license = StaticMapping(verbose_license)
        # IF license IS An SPDX ID
        IsSPDX = IsAnSPDX(license)
        if IsSPDX:
            print(license+" is an SPDX-id")
            return license
    # if verbose license IS NOT within aliases - run dynamic mapping
    else:
        license_names = []
        license_name = DynamicMapping(verbose_license)
        print("Dynamic mapping result: ")
        print(license_name)
        IsAnAlias = IsInAliases(license_name)
        if IsAnAlias:
            print(license_name)
            license_mapped = StaticMapping(license_name)
            IsSPDX = IsAnSPDX(license_mapped)
            if IsSPDX:
                print(license_mapped+" is an SPDX-id")
                return license_mapped
        else:
            return license_name


def StaticMappingList(InboundLicenses_cleaned):
    print(InboundLicenses_cleaned)
    CSVfilePath = "../../csv/spdx-id.csv"
    InboundLicenses_SPDX = []
    column_names_list = ['Scancode', 'SPDX-ID']
    df = CSV_to_dataframe(CSVfilePath, column_names_list)
    df = df.set_index('Scancode')
    for license in InboundLicenses_cleaned:
        newElement = df.loc[license]['SPDX-ID']
        if newElement is not np.nan:
            InboundLicenses_SPDX.append(newElement)
        else:
            InboundLicenses_SPDX.append(license)
    return InboundLicenses_SPDX


def DetectWithAcronyms(verbose_license):
    licenseVersion = None
    licenseName = None
    supposedLicense = None
    only = False
    orLater = False

    list_of_words = verbose_license.split()
    for word in list_of_words:
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
    matchObj = re.match(pattern, licenseVersion)
    if matchObj:
        licenseVersion = licenseVersion.replace('v', '')
        return licenseVersion
    else:
        return licenseVersion


def DetectWithKeywords(verbose_license):
    # probably you could declare globally these variables - inasmuch it is also used by the DetectWithAcronyms() function
    licenseVersion = None
    licenseName = None
    supposedLicense = None
    orLater = False
    only = False
    DynamicMappingKeywordsList = [
        "2010", "2014", "academic", "affero", "attribution", "berkeley", "bsd", "bzip", "classpath", "clear", "cmu", "cpe", "commons", "creative", "database", "distribution", "eclipse", "epl", "eupl", "european",
        "exception","expat", "general", "ibm", "later", "lesser","lgpl", "libpng", "library", "license", "miros", "mozilla", "modification", "mpi", "mpl", "ntp", "new", "nuclear", "national", "only", "open", "openssl", "patent", "psf","psfl", "python",
        "png", "power", "powerpc", "public", "permissive", "qhull", "reciprocal", "shortened","simplified","software", "tiff", "uc", "universal",
        "upl", "views", "warranty", "zlib", "zero",]

    MappedKeywords = list()
    list_of_words = verbose_license.split()
    for word in list_of_words:
        if '-' in word:
            words = word.replace('-', ' ')
            strings = words.split()
            for string in strings:
                list_of_words.append(string)

    #check with keywords
    for word in list_of_words:
        # check case insesitive starting with v words, to catch vX.X cases.
        if bool(re.match('v', word, re.I)):
            word = ConformVersionNumber(word)
        if "(" or ")" or "[" or "]" in word:
            word = re.sub(r"[()]", "", word)
            word = re.sub(r"[\[\]]", "", word)
        print("After running ConformVersionNumber: "+word)
        if word.lower() in DynamicMappingKeywordsList:
            MappedKeywords.append(word.lower())
        if word in versions:
            print(word)
            licenseVersion = str(word)
            if licenseVersion == "1" or "2" or "3" or "4" or "5":
                licenseVersion = str(float(licenseVersion))
            MappedKeywords.append(licenseVersion)
    print("Mapped Keywords:")
    print(MappedKeywords)
    #If there are keywords matched
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
                    print("inside or later")
                    return licenseName
            if only:
                if licenseVersion == "2.0" or licenseVersion == "2.1" or licenseVersion == "3.0":
                    licenseName = "LGPL-"+licenseVersion+"-only"
                    print("inside only")
                    return licenseName

        if ("general" in MappedKeywords) and (("affero" and "lesser" and "library") not in MappedKeywords):# and "lesser" not in MappedKeywords:
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


def DynamicMapping(verbose_license):
    detectedWithAcronymsLicense = DetectWithAcronyms(verbose_license)
    IsSPDX = IsAnSPDX(detectedWithAcronymsLicense)

    if IsSPDX:
        print(detectedWithAcronymsLicense+" is an SPDX-id")
        return detectedWithAcronymsLicense
    IsAnAlias = IsInAliases(detectedWithAcronymsLicense)
    if IsAnAlias:
        print(detectedWithAcronymsLicense)
        detectedWithAcronymsLicense = StaticMapping(
            detectedWithAcronymsLicense)
        IsSPDX = IsAnSPDX(detectedWithAcronymsLicense)
        if IsSPDX:
            print(detectedWithAcronymsLicense+" is an SPDX-id")
            return detectedWithAcronymsLicense

    detectedWithKeywordsLicense = DetectWithKeywords(verbose_license)
    IsSPDX = IsAnSPDX(detectedWithKeywordsLicense)
    if IsSPDX:
      print(detectedWithKeywordsLicense+" is an SPDX-id")
      return detectedWithKeywordsLicense
    IsAnAlias = IsInAliases(detectedWithKeywordsLicense)
    if IsAnAlias:
      print(detectedWithKeywordsLicense)
      detectedWithKeywordsLicense = StaticMapping(detectedWithKeywordsLicense)
      IsSPDX = IsAnSPDX(detectedWithKeywordsLicense)
      if IsSPDX:
          print(detectedWithKeywordsLicense+" is an SPDX-id")
          return detectedWithKeywordsLicense
    if not IsAnAlias:
        return verbose_license

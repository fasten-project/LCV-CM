#!/usr/bin/python
# import urllib.request
import re

from LCVlib.CommonLists import licenses, versions, literalVersions, NumberDict, DynamicMappingKeywordsList, list_of_parenthesis, LicenseLetterVersion

from LCVlib.CheckAliasAndSPDXId import IsAnSPDX, ConformWithSPDX

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
            # to prevent crashes on cases where V is the last letter.
            if len(strings)>1:
                word2 = strings[1]
                # check if after 'v' there is a digit
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
        if not startWithV:
            list_of_words = detectV(list_of_words,word)
        if startWithV:
            word = ConformVersionNumber(word)
            if word.isdigit():
                licenseVersion=word
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
        #here the space in " " is fundamental, or not the licenseName will never be splitted later.
        licenseNameV = licenseNameV.sub(" ", licenseName)
        licenseName = licenseNameV
        return licenseName
    else:
        return licenseName

def SeparateLicenseNameAndVersionNumber(licenseName):
    pattern = '[Aa-zZ]+[0-9].?[0-9]?'
    matchObj = re.match(pattern, licenseName,re.IGNORECASE)
    if matchObj:
        print(licenseName+"inside matchObj")
        # Add a space between license name and version
        res = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", licenseName)
        return res
    else:
        return licenseName

def RemoveParenthesisAndSpecialChars(verbose_license):
    # remove special characters from the end of the word
    endingSpecChars= '[,!.?](?:\s+)?$'
    while(re.findall(endingSpecChars, verbose_license)):
        verbose_license = re.sub(endingSpecChars,'', verbose_license)
        print(verbose_license)
    for char in list_of_parenthesis:
        if char in verbose_license:
            verbose_license = verbose_license.replace(char, '')
    return verbose_license



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
        if IsAnSPDX(word):
            word = ConformWithSPDX(word)
            return word
        if not IsAnSPDX(word) and '-' in word:
            print("inside removal - ")
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
        if "academic" in MappedKeywords:
            licenseName = "AFL"
        # this check should consider also 2-1.0.5 ..
        if "bzip" in MappedKeywords or "2010" in MappedKeywords:
            licenseName = "bzip2-1.0.6"
            return licenseName
        if "apache" in MappedKeywords:
            if licenseVersion == "2.0":
                licenseName = "Apache-2.0"
            return licenseName
        if "beer" in MappedKeywords:
            licenseName = "Beerware"
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
        if "cecill" in MappedKeywords:
            print("inside cecill")
            if "b" in MappedKeywords:
                licenseName = "CECILL-B"
                return licenseName
            if "c" in MappedKeywords:
                licenseName = "CECILL-C"
                return licenseName
            if licenseVersion in versions:
                licenseName = "CECILL-"+licenseVersion
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
        if "reciprocal" in MappedKeywords:
            if "public" in MappedKeywords and "license" in MappedKeywords:
                if licenseVersion == "1.5":
                    licenseName = "RPL-1.5"
                    return licenseName
                if licenseVersion == "1.1":
                    licenseName = "RPL-1.1"
                    return licenseName
            if "microsoft" in MappedKeywords:
                licenseName = "MS-RL"
                return licenseName
        if "microsoft" in MappedKeywords:
            if "reciprocal" in MappedKeywords:
                licenseName = "MS-RL"
                return licenseName
            if "public" in MappedKeywords:
                licenseName = "MS-PL"
                return licenseName
        if "unlicense" in MappedKeywords:
            licenseName = "Unlicense"
        if "iscl" in MappedKeywords:
            licenseName = "ISC"
            return licenseName
        if "affero" in MappedKeywords:
            licenseName = "AGPL"
        if "agpl" in MappedKeywords:
            licenseName = "AGPL"
            if licenseVersion in licenses:
                if orLater:
                    licenseName = "AGPL-"+licenseVersion+"-or-later"
                    return licenseName
                else:
                    licenseName = "AGPL-"+licenseVersion+"-only"
                    return licenseName

        if "library" in MappedKeywords or "lesser" in MappedKeywords or "lgpl" in MappedKeywords:
            licenseName = "LGPL"
            if orLater:
                if licenseVersion == "2.0" or licenseVersion == "2.1" or licenseVersion == "3.0":
                    licenseName = "LGPL-"+licenseVersion+"-or-later"
                    return licenseName
            if licenseVersion == "2.0" or licenseVersion == "2.1" or licenseVersion == "3.0":
                licenseName = "LGPL-"+licenseVersion+"-only"
                return licenseName
        if "gpl" in MappedKeywords or "general" or "gnu" in MappedKeywords and "affero" not in MappedKeywords and "lesser" not in MappedKeywords and "library" not in MappedKeywords:
            licenseName = "GPL"
            if orLater:
                if licenseVersion == "2.0" or licenseVersion == "2.1" or licenseVersion == "3.0":
                    licenseName = "GPL-"+licenseVersion+"-or-later"
                    return licenseName
            if licenseVersion == "2.0" or licenseVersion == "2.1" or licenseVersion == "3.0":
                licenseName = "GPL-"+licenseVersion+"-only"
                return licenseName

        if "general" in MappedKeywords and "affero" not in MappedKeywords and "lesser" not in MappedKeywords and "library" not in MappedKeywords:
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

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

licenses = ["AFL","AGPL","Apache","Artistic","BSD","BSL","bzip2","CC0","CDDL","CPL","curl","EFL","EPL","EUPL","FTL","GPL","HPND","IBM","ICU","IJG","IPL","ISC",
"LGPL","Libpng","libtiff","MirOS","MIT","CMU","MPL","MS","NBPL","NTP","OpenSSL","OSL","Python","Qhull","RPL","SunPro","Unicode","UPL","WTFPL","X11","XFree86","Zlib","zlib-acknowledgement"]
versions = ["1.0","1.0.5","1.0.6","1.1","1.5","2.0","2.1","3.0","3.1","1","2","3","4","5"]


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
            if single_verbose_license == row[0]: # if the username shall be on column 3 (-> index 2)
                print (single_verbose_license+" is a recognized Alias")
                IsInAliases = True
                return IsInAliases
        if not IsInAliases:
            print (single_verbose_license+" is a not recognized Alias")
            return IsInAliases

def StaticMapping(single_verbose_license):
    #1540 entries
    CSVfilePath = "../../csv/spdx-id.csv"
    column_names_list = ['Scancode', 'SPDX-ID']
    df = CSV_to_dataframe(CSVfilePath, column_names_list)
    df = df.set_index('Scancode')
    #IsAnAlias = False
    # @Michele you should insert a check upon the column of "scancode name",
    # if the license is there, enter the cycle
    # if not, run the Dynamic Method. <--- this is done in ConvertToSPDX function
    ##########################################################
    # After the dynamic method, a keyerror should be handled
    # you should provide an output without producing a KeyError <--- still should be handled
    single_verbose_license_SPDX_id = df.loc[single_verbose_license]['SPDX-ID']
    if single_verbose_license_SPDX_id is not np.nan:
        return single_verbose_license_SPDX_id
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
        if IsSPDX :
            print(license+" is an SPDX-id")
            return license
    # if verbose license IS NOT within aliases - run dynamic mapping
    else:
        license_names = []
        license_name = DynamicMapping(verbose_license)
        #print("After dynamicMapping in ConvertToSPDX")
        print("Dynamic mapping result: ")
        print(license_name)
        IsAnAlias = IsInAliases(license_name)
        if IsAnAlias:
            print(license_name)
            license_mapped = StaticMapping(license_name)
            IsSPDX = IsAnSPDX(license_mapped)
            if IsSPDX :
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

def DynamicMapping(verbose_license):
    licenseVersion = None
    licenseName = None
    orLater=False
    only=False
    IsAnAlias=False
    IsSPDX=False
    supposedLicenseSPDX = None
    supposedLicense = None
    affero=False
    lesser=False
    general=False
    academic=False
    distribution=False
    bzip=False
    powerpc=False
    tiff=False
    miros=true

    list_of_words = verbose_license.split()
    for word in list_of_words:
        if word in licenses:
            licenseName=word
        if word in versions:
            licenseVersion=word
            if licenseVersion == "1" or "2" or "3" or "4" or "5":
                print("License version:")
                licenseVersion=str(float(licenseVersion))
                print(licenseVersion)

        if word == "Later" or word == "later":
            orLater=True
        if word == "Only" or word == "only":
            only=True
        if word == "Affero" or word == "affero":
            affero=True
        if word == "Lesser" or word == "lesser":
            lesser=True
        if word == "General" or word == "general":
            general=True
        if word == "Academic" or word == "academic":
            academic=True
        if word == "Distribution" or word == "distribution":
            distribution=True
        if word == "2010":
            bzip=True
        if word == "PowerPC" or word == "powerpc" or word == "Power" or word == "power":
            powerpc=True
        if word == "tiff" or word == "Tiff" or word == "TIFF":
            tiff=True
        if word == "MirOS" or word == "mirOS" or word == "Miros" or word == "miros":
            miros=False

    # after scanning the whole verbose license
    if academic:
        licenseName = "AFL"
    if bzip:
        licenseName = "bzip2-1.0.6"
    if distribution:
        licenseName = "CDDL"
    if powerpc:
        licenseName = "IBM-pibs"
    if tiff:
        licenseName = "libtiff"
    if miros:
        licenseName = "MirOS"
    if affero:
        licenseName = "AGPL"
    if lesser:
        licenseName = "LGPL"
    if general and not affero and not lesser:
        licenseName = "GPL"
    if licenseName is not None and licenseVersion is None:
        supposedLicense = licenseName
        supposedLicenseSPDX = licenseName
    if not orLater and not only:
        if licenseName and licenseVersion is not None:
            supposedLicense = licenseName+" "+licenseVersion
            #supposedLicenseSPDX = licenseName+"-"+licenseVersion
    if orLater:
        if licenseName and licenseVersion is not None:
            supposedLicense = licenseName+" "+licenseVersion+" or later"
            #supposedLicenseSPDX = licenseName+"-"+licenseVersion+"-or-later"
    if only:
        if licenseName and licenseVersion is not None:
            supposedLicense = licenseName+" "+licenseVersion+" only"
            #supposedLicenseSPDX = licenseName+"-"+licenseVersion+"-only"
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

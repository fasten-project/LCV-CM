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
from LCVlib.VerboseLicenseParsing import DetectWithAcronyms, DetectWithKeywords, ConformVersionNumber
from LCVlib.CommonLists import *
'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''


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
            if single_verbose_license == row[0]:
                print(single_verbose_license+" is a recognized Alias")
                IsInAliases = True
                return IsInAliases
        if not IsInAliases:
            #print(single_verbose_license+" is a not recognized Alias")
            return IsInAliases


def StaticMapping(single_verbose_license):
    CSVfilePath = "../../csv/spdx-id.csv"
    column_names_list = ['Scancode', 'SPDX-ID']
    df = CSV_to_dataframe(CSVfilePath, column_names_list)
    df = df.set_index('Scancode')
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
        if IsSPDX:
            print(license+" is an SPDX-id")
            return license
    # if verbose license IS NOT within aliases - run dynamic mapping
    else:
        print("inside else DynamicMapping")
        print(verbose_license)
        #license_names = []
        license_name = DynamicMapping(verbose_license)
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


def StaticMappingList(InboundLicenses_cleaned):
    #print(InboundLicenses_cleaned)
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
    detectedWithAcronymsLicense = DetectWithAcronyms(verbose_license)
    print("After decteting with acronyms")
    print(detectedWithAcronymsLicense)
    detectedWithAcronymsLicense= MappingResultCheck(detectedWithAcronymsLicense)
    IsSPDX = IsAnSPDX(detectedWithAcronymsLicense)
    print(IsSPDX)
    if IsAnSPDX(detectedWithAcronymsLicense):
        print("Is an SPDX id inside of Dynamic Mapping . It should then exit")
        return detectedWithAcronymsLicense
    else:
        detectedWithKeywordsLicense = DetectWithKeywords(verbose_license)
        MappingResultCheck(detectedWithKeywordsLicense)
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

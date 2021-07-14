#!/usr/bin/python
# import urllib.request
import requests
import json
import time
import sys
import pandas as pd
import numpy as np
from LCVlib.SPDXIdMapping import StaticMapping, DynamicMapping, ConvertToSPDX, IsAnSPDX

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


def CSV_to_dataframeOSADL(CSVfilePath):
    """
    Import a CSV and transform it into a pandas dataframe avoiding to add row numbers.
    """
    df = pd.read_csv(CSVfilePath, index_col=0)
    '''
    # With this method we can create the transpose of OSADL Matrix, but require to add "License" keyword at the top of the Matrix
    df = df.transpose()
    df.to_csv(r'/home/michelescarlato/gitrepo/LCV-CM-Fasten/LCV-CM/csv/OSADL_transposed.csv',
              index=True, header=True)
              '''
    return df

# create a list of licenses presents in the OSADL matrix
df = CSV_to_dataframeOSADL("../../csv/OSADL.csv")
supported_licenses_OSADL = list(df.index)
print(supported_licenses_OSADL)
# create a list of licenses presents in our original matrix

def verifyOSADL_Transposed(CSVfilePath, InboundLicenses_cleaned, OutboundLicense):
    verificationList = list()
    if (OutboundLicense in supported_licenses_OSADL):
        column_names_list = [OutboundLicense]
        column_names_list.insert(0, 'License')
        # df = CSV_to_dataframe(CSVfilePath, column_names_list)
        # Column_array = df.to_numpy()
        # retrieve data from CSV file
        CSVfilePath = "../../csv/OSADL_transposed.csv"
        df = CSV_to_dataframe(CSVfilePath, column_names_list)
        df = df.set_index('License')
        if (len(InboundLicenses_cleaned) == 1) and (InboundLicenses_cleaned[0] == OutboundLicense):
            output = "For this project only " + \
                InboundLicenses_cleaned[0] + \
                " as the inbound license has been detected, and it is the same of the outbound license (" + \
                OutboundLicense+"), implying that it is compatible. \nIt means that it is license compliant. "
            verificationList.append(output)
            return verificationList
        for license in InboundLicenses_cleaned:
            if (license in supported_licenses_OSADL):
                comparison = df.loc[license, OutboundLicense]
                if comparison == "No":
                    output = license+" is not compatible with " + \
                        OutboundLicense+" as an outbound license."
                    verificationList.append(output)
                if comparison == "Yes":
                    output = license+" is compatible with " + \
                        OutboundLicense + " as an outbound license."
                    verificationList.append(output)
                # OSADL Matrix could be shipped with empty field, resulting in nan.
                if comparison == "-":
                    output = license+" is compatible with " + \
                        OutboundLicense + " as an outbound license."
                    verificationList.append(output)
                if comparison == "?":
                    output = "There is insufficient information or knowledge whether the "+license+" as inbound license" + \
                        " is compatible with the " + OutboundLicense + " as outbound license. Therefore a general recommendation" + \
                        " on the compatibility of "+license+" as inbound with the " + \
                        OutboundLicense+" as outbound cannot be given."
                    verificationList.append(output)
                if comparison == "Dep.":
                    output = "Depending compatibility of the "+license+" with the " + \
                        OutboundLicense + " license is explicitly stated in the " + \
                        OutboundLicense+" license checklist hosted by OSADL.org"
                    verificationList.append(output)
            else:
                output = "The inbound license "+license+" is not present in the Compatibility Matrix"
                verificationList.append(output)
    return verificationList

def verifyFlag(CSVfilePath, InboundLicenses_cleaned, OutboundLicense):
    verificationFlagList = list()

    if (OutboundLicense in supported_licenses_OSADL):

        column_names_list = [OutboundLicense]
        column_names_list.insert(0, 'License')
        # retrieve data from CSV file
        df = CSV_to_dataframe(CSVfilePath, column_names_list)
        df = df.set_index('License')
        if (len(InboundLicenses_cleaned) == 1) and (InboundLicenses_cleaned[0] == OutboundLicense):
            verificationFlag = True
            return verificationFlag

        for license in InboundLicenses_cleaned:
            if (license in supported_licenses_OSADL):
                comparison = df.loc[license, OutboundLicense]
                if comparison == "No":
                    verificationFlag = False
                    return verificationFlag
                if comparison == "Yes":
                    verificationFlag = True
                    verificationFlagList.append(verificationFlag)
                if comparison == "-":
                    verificationFlag = True
                    verificationFlagList.append(verificationFlag)
                if comparison == "?":
                    verificationFlag = "DUC"
                    verificationFlagList.append(verificationFlag)
                if comparison == "Dep.":
                    verificationFlag = "DUC"
                    verificationFlagList.append(verificationFlag)
            else:
                output = "The inbound license "+license+" is not present in the Compatibility Matrix"
                verificationFlagList.append(output)
                #simple output single line
                #return output
                #output containing all the flags, including the missing license
                return verificationFlagList

        if ("DUC" in verificationFlagList):
            verificationFlag = "DUC"
            return verificationFlag
        if all(verificationFlagList):
            verificationFlag = True
            return verificationFlag
        else:
            verificationFlag = False
            return verificationFlag
    else:
        output = "The outbound license "+OutboundLicense+" is not present in the Compatibility Matrix"
        verificationFlagList.append(output)
        return verificationFlagList


def retrieveOutboundLicense(url):
    print("Retrieving outbound license from: "+url)
    response = requests.get(url).json()
    OutboundLicense = response['license']['spdx_id']
    if OutboundLicense == "NOASSERTION":
        print(OutboundLicense)
        print("Outbound noassertion")
    else:
        print("Outbound license: "+OutboundLicense)

    return OutboundLicense


def CompareSPDX(InboundLicenses_SPDX, OutboundLicense):
    if len(InboundLicenses_SPDX) == 1:
        print("The SPDX id for the only inbound license detected is:")
        print(InboundLicenses_SPDX[0])
    else:
        print("The SPDX IDs for the inbound licenses found are:")
        print(InboundLicenses_SPDX)
    print("#################")
    print("Running the license compliance verification:")
    print("Inbound license list :\n"+str(InboundLicenses_SPDX))
    print("The outbound license is: "+OutboundLicense)
    CSVfilePath = "../../csv/licenses_tests.csv"
    verificationList = verifyOSADL_Transposed(
        CSVfilePath, InboundLicenses_SPDX, OutboundLicense)
    verificationList = parseVerificationList(verificationList)
    return verificationList


def CompareSPDX_OSADL(InboundLicenses_SPDX, OutboundLicense):
    #InboundLicenses_SPDX = Mapping(InboundLicenses_SPDX)
    if len(InboundLicenses_SPDX) == 1:
        print("The SPDX id for the only inbound license detected is:")
        print(InboundLicenses_SPDX[0])
    else:
        print("The SPDX IDs for the inbound licenses found are:")
        print(InboundLicenses_SPDX)
    print("#################")
    print("Running the license compliance verification:")
    print("Inbound license list :\n"+str(InboundLicenses_SPDX))
    print("The outbound license is: "+OutboundLicense)
    #CSVfilePath = "../../csv/licenses_tests.csv"
    CSVfilePath = "../../csv/OSADL_transposed.csv"
    verificationList = verifyOSADL_Transposed(
        CSVfilePath, InboundLicenses_SPDX, OutboundLicense)
    verificationList = parseVerificationList(verificationList)
    return verificationList

def Compare_OSADL(InboundLicenses, OutboundLicense):
    print(InboundLicenses)
    InboundLicenses_SPDX=[]
    for license in InboundLicenses:
        IsSPDX= IsAnSPDX(license)
        print("Is "+license+" an SPDX?")
        print(IsSPDX)
        if not IsSPDX:
            license_spdx = ConvertToSPDX(license)
            print("dentro for ")
            print(license_spdx)
            InboundLicenses_SPDX.append(license_spdx)
        else:
            InboundLicenses_SPDX.append(license)
    print("InboundLicenses_SPDX:")
    print(InboundLicenses_SPDX)
    IsSPDX=IsAnSPDX(OutboundLicense)
    if not IsSPDX:
        OutboundLicense_SPDX = ConvertToSPDX(OutboundLicense)
    else:
        OutboundLicense_SPDX = OutboundLicense

    if len(InboundLicenses_SPDX) == 1:
        print("The SPDX id for the only inbound license detected is:")
        print(InboundLicenses_SPDX[0])
    else:
        print("The SPDX IDs for the inbound licenses found are:")
        print(InboundLicenses_SPDX)
    print("#################")
    print("Running the license compliance verification:")
    print("Inbound license list :\n"+str(InboundLicenses_SPDX))
    print("The outbound license is: "+OutboundLicense_SPDX)
    #CSVfilePath = "../../csv/licenses_tests.csv"
    CSVfilePath = "../../csv/OSADL_transposed.csv"
    verificationList = verifyOSADL_Transposed(
        CSVfilePath, InboundLicenses_SPDX, OutboundLicense_SPDX)
    verificationList = parseVerificationList(verificationList)
    return verificationList



def CompareSPDXFlag(InboundLicenses_SPDX, OutboundLicense):
    if len(InboundLicenses_SPDX) == 1:
        print("The SPDX id for the only inbound license detected is:")
        print(InboundLicenses_SPDX[0])
    else:
        print("The SPDX IDs for the inbound licenses found are:")
        print(InboundLicenses_SPDX)
    print("#################")
    print("Running the license compliance verification:")
    print("Inbound license list :\n"+str(InboundLicenses_SPDX))
    print("The outbound license is: ", OutboundLicense)
    CSVfilePath = "../../csv/OSADL_transposed.csv"
    verificationFlag = verifyFlag(
        CSVfilePath, InboundLicenses_SPDX, OutboundLicense)
    return verificationFlag


def parseVerificationList(verificationList):
    notCompatible = "is not compatible"
    Compatible = "is compatible"
    isNotSupported = "is not supported"
    TBD = "compatibility with"
    UNK = "UNKNOWN"
    II = "II"
    DEP = "DEP"
    DUC = "DUC"

    for element in verificationList:
        if notCompatible in element:
            print("YOUR PACKAGE IS NOT COMPLIANT because:\n"+element)
        if Compatible in element:
            print(
                "\n"+element+"\nThis allow you to use this inbound license in your package.\n")
        if isNotSupported in element:
            print("\n"+element
                  + "\nMomentairly 'or later' notation are not supported.\n")
        if TBD in element:
            print(
                "\n"+element+"\nThis compatibility association still need to be defined.\n")
        if UNK in element:
            print("\n"+element)
        if II in element:
            print("\n"+element+"\nThere is insufficient information or knowledge upon this compatibility. OSADL Matrix is not able to compare them.\n")
        if DEP in element:
            print("\n"+element+"\nDepending compatibility is explicitly stated in the license checklist hosted by OSADL.org")
        if DUC in element:
            print("\n"+element+"\nDepending on the use case.")

        # if all element are compatible, license compliance occurs.
        indexLicense = 0
        for element in verificationList:
            if Compatible in element:
                indexLicense += 1
        print(str(indexLicense)+" above "+str(len(verificationList))
              + " licenses found are compatible.")
        if indexLicense == len(verificationList):
            print("Hence your project is compatible.")
        else:
            print("Hence your project is not compatible.")
        return verificationList

#!/usr/bin/python
# import urllib.request
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
orLater = "or-later"


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
#print(supported_licenses_OSADL)
# create a list of licenses presents in our original matrix
df = CSV_to_dataframeOSADL("../../csv/licenses_tests.csv")
supported_licenses = list(df.index)
#print(supported_licenses)

def verifyOSADL_Transposed(CSVfilePath, InboundLicenses_cleaned, OutboundLicense):
    verificationList = list()
    if (OutboundLicense in supported_licenses_OSADL):
        column_names_list = [OutboundLicense]
        column_names_list.insert(0, 'License')
        df = CSV_to_dataframe(CSVfilePath, column_names_list)
        Column_array = df.to_numpy()
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
            if (license in Column_array):
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


def verifyOSADL(CSVfilePath, InboundLicenses_cleaned, OutboundLicense):
    verificationList = list()
    if (OutboundLicense in supported_licenses_OSADL):
        # retrieve data from CSV file
        df = CSV_to_dataframeOSADL(CSVfilePath)

        if (len(InboundLicenses_cleaned) == 1) and (InboundLicenses_cleaned[0] == OutboundLicense):
            output = "For this project only " + \
                InboundLicenses_cleaned[0] + \
                " as the inbound license has been detected, and it is the same of the outbound license (" + \
                OutboundLicense+"), implying that it is compatible. \nIt means that it is license compliant. "
            verificationList.append(output)
            return verificationList
        else:
            for license in InboundLicenses_cleaned:
                if (license in supported_licenses_OSADL):
                    comparison = df.loc[OutboundLicense, str(license)]
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


def RetrieveInboundLicenses(JSONPath):
    print("Retrieving inbound license(s) from: "+JSONPath)
    print("Started Reading the JSON report")
    with open(JSONPath, "r") as read_file:
        print("Reading: " + JSONPath)
        data = json.load(read_file)  # dict
        InboundLicenses = []
        for i in data['payload']['fileMetadata']:
            for x in (i['licenses']):
                if x not in InboundLicenses:
                    InboundLicenses.append(x)
    print("Finished reading the JSON report")
    print("These inbound licenses have been found:")
    print(InboundLicenses)

    print("###################")
    return InboundLicenses


def SPDXIdMapping(InboundLicenses_cleaned):
    CSVfilePath = "../../csv/spdx-id.csv"
    InboundLicenses_SPDX = []
    column_names_list = ['Scancode', 'SPDX-ID']
    df = CSV_to_dataframe(CSVfilePath, column_names_list)
    df = df.set_index('Scancode')
    for license in InboundLicenses_cleaned:
        newElement = df.loc[license]['SPDX-ID']
        if newElement is not np.nan:
            # print(newElement)
            InboundLicenses_SPDX.append(newElement)
            if orLater in newElement:
                print("The usage of 'or later' is not supported. \n Please specify a license version instead of using 'or later' notation.")
        else:
            InboundLicenses_SPDX.append(license)
        # print(InboundLicenses_cleaned)

    return InboundLicenses_SPDX


def verify(CSVfilePath, InboundLicenses_cleaned, OutboundLicense):
    verificationList = list()
    if (OutboundLicense in supported_licenses):
        column_names_list = [OutboundLicense]
        column_names_list.insert(0, 'License')
        # retrieve data from CSV file
        df = CSV_to_dataframe(CSVfilePath, column_names_list)
        df = df.set_index('License')
        if (len(InboundLicenses_cleaned) == 1) and (InboundLicenses_cleaned[0] == OutboundLicense):
            output = "For this project only " + \
                InboundLicenses_cleaned[0] + \
                " as the inbound license has been detected, and it is the same of the outbound license (" + \
                OutboundLicense+"), implying that it is compatible. \nIt means that it is license compliant. "
            verificationList.append(output)
            return verificationList
        else:
            for license in InboundLicenses_cleaned:
                if (license in supported_licenses):
                    comparison = df.loc[license, OutboundLicense]
                    if comparison == "0":
                        output = license+" is not compatible with " + \
                            OutboundLicense+" as an outbound license."
                        verificationList.append(output)
                    if comparison == "NS":
                        output = license+" is not supported, because 'or later' notation."
                        verificationList.append(output)
                    if comparison == "1":
                        output = license+" is compatible with " + \
                            OutboundLicense + " as an outbound license."
                        verificationList.append(output)
                    if comparison == "-":
                        output = license+" is compatible with " + \
                            OutboundLicense + " as an outbound license."
                        verificationList.append(output)
                    if comparison == "TBD":
                        output = license+" compatibility with " + \
                            OutboundLicense + " still needs to be defined."
                        verificationList.append(output)
                    if comparison == "UNK":
                        output = "An UNKNOWN license has been found within the project. This cannot reveal license incompatibility"
                        verificationList.append(output)
                    if comparison == "II":
                        output = "There is insufficient information or knowledge whether the "+license+" as inbound license" + \
                            " is compatible with the " + OutboundLicense + " as outbound license. Therefore a general recommendation" + \
                            " on the compatibility of "+license+" as inbound with the " + \
                            OutboundLicense+" as outbound cannot be given."
                        verificationList.append(output)
                    if comparison == "DEP":
                        output = "Depending compatibility of the "+license+" with the " + \
                            OutboundLicense + " license is explicitly stated in the " + \
                            OutboundLicense+" license checklist hosted by OSADL.org"
                        verificationList.append(output)
                else:
                    output = "The inbound license "+license+" is not present in the Compatibility Matrix"
                    verificationList.append(output)
    else:
        output = "The outbound license "+OutboundLicense+"  is not present in the Compatibility Matrix"
        verificationList.append(output)
    return verificationList


def verifyFlag(CSVfilePath, InboundLicenses_cleaned, OutboundLicense):
    column_names_list = [OutboundLicense]
    column_names_list.insert(0, 'License')
    verificationFlagList = list()
    # retrieve data from CSV file
    df = CSV_to_dataframe(CSVfilePath, column_names_list)
    df = df.set_index('License')
    if (len(InboundLicenses_cleaned) == 1) and (InboundLicenses_cleaned[0] == OutboundLicense):
        verificationFlag = True
        return verificationFlag

    for license in InboundLicenses_cleaned:
        comparison = df.loc[license, OutboundLicense]
        if comparison == "0":
            verificationFlag = False
            return verificationFlag
        if comparison == "NS":
            verificationFlag = False
            return verificationFlag
        if comparison == "1":
            verificationFlag = True
            verificationFlagList.append(verificationFlag)
        if comparison == "-":
            verificationFlag = True
            verificationFlagList.append(verificationFlag)
        if comparison == "TBD":
            verificationFlag = False
            return verificationFlag
        if comparison == "UNK":
            verificationFlag = False
            return verificationFlag
        if comparison == "II":
            verificationFlag = "DUC"
            verificationFlagList.append(verificationFlag)
        if comparison == "DEP":
            verificationFlag = "DUC"
            verificationFlagList.append(verificationFlag)
    if ("DUC" in verificationFlagList):
        verificationFlag = "DUC"
        return verificationFlag
    if all(verificationFlagList):
        verificationFlag = True
        return verificationFlag
    else:
        verificationFlag = False
        return verificationFlag


def CheckOutboundLicense(OutboundLicense):
    if OutboundLicense != "NOASSERTION":
        print("The outbound license for the project is: "+OutboundLicense)

        if orLater in OutboundLicense:
            print("The usage of `'or later' is not supported. \n Please specify a license version instead of using `'or later'` notation.")
            return
    else:
        print("This project does not specify correctly an SPDX id for its oubound license")
        return
    return OutboundLicense


def Compare(InboundLicenses, OutboundLicense):
    print("Running SPDXid mapping function:")
    InboundLicenses_SPDX = SPDXIdMapping(InboundLicenses)

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
    CSVfilePath = "../../csv/licenses_tests.csv"
    verificationListToParse = verify(
        CSVfilePath, InboundLicenses_SPDX, OutboundLicense)
    verificationList = parseVerificationList(verificationListToParse)
    return verificationList


def CompareFlag(InboundLicenses, OutboundLicense):
    print("Running SPDXid mapping function:")
    InboundLicenses_SPDX = SPDXIdMapping(InboundLicenses)

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
    CSVfilePath = "../../csv/licenses_tests.csv"
    verificationFlag = verifyFlag(
        CSVfilePath, InboundLicenses_SPDX, OutboundLicense)
    return verificationFlag


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
    verificationList = verify(
        CSVfilePath, InboundLicenses_SPDX, OutboundLicense)
    verificationList = parseVerificationList(verificationList)
    return verificationList


def CompareSPDX_OSADL(InboundLicenses_SPDX, OutboundLicense):
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
    CSVfilePath = "../../csv/OSADL.csv"
    verificationList = verifyOSADL(
        CSVfilePath, InboundLicenses_SPDX, OutboundLicense)
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
    CSVfilePath = "../../csv/licenses_tests.csv"
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


def runtimer(t):
    print("###############################################")
    print("tasks done, now sleeping for "+str(t)+" seconds")
    for i in range(t, 0, -1):
        sys.stdout.write(str(i)+' ')
        sys.stdout.flush()
        time.sleep(1)
    print("\n")

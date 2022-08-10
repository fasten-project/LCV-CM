from LCVlib.SPDXIdMapping import StaticMappingList,IsAnSPDX,StaticMapping,DynamicMapping,IsInAliases,ConvertToSPDX
from LCVlib.VerboseLicenseParsing import RemoveParenthesisAndSpecialChars
from PYPI_license_collector import RetrievePypiLicenseInformationPackage, APICallConvertToSPDX, APICallIsAnSPDX, appendToFile
from LCVlib.CommonLists import *
import re
import os
from itertools import tee
#import pandas as pd

#counters


txt_list = []
base_dir = ("/home/michelescarlato/gitrepo/LCV-CM/src/LCV/collectingPypiLicenses/output/already_parsed")
def scandir():
    not_converted = 0
    converted = 0
    already_SPDX = 0
    none_license = 0
    not_found = 0
    #not_converted_list = []
    os.chdir("/src/LCV/collectingPypiLicenses/output/already_parsed")
    for dirpath, dirnames, filename in os.walk(base_dir):
        for filename in filename:
            # create full path
            txtfile_full_path = os.path.join(dirpath, filename)
            with open(txtfile_full_path) as f:
                lines = f.readlines()
                for line in lines:
                    if "NOT Converted." in line:
                        not_converted += 1
                        pass
                    if "Converted." in line:
                        converted += 1
                        pass
                    if "Pypi provided an SPDX id." in line:
                        already_SPDX += 1
                        pass
                    if "detected pypi license: None" in line:
                        none_license += 1
                        pass
                    if "404 - page not found" in line:
                        not_found += 1
                        pass


    total_packages = not_converted + converted + already_SPDX + none_license + not_found
    print(f'''
    Not converted: {not_converted}
    Converted : {converted}
    Already SPDX : {already_SPDX}
    None license : {none_license}
    404 not found : {not_found}
    Total packages analyzed: {total_packages}
    ''')


def not_converted_list():
    not_converted_list = []
    os.chdir("/src/LCV/collectingPypiLicenses/output/already_parsed")
    for dirpath, dirnames, filename in os.walk(base_dir):
        for filename in filename:
            # create full path
            txtfile_full_path = os.path.join(dirpath, filename)
            with open(txtfile_full_path) as f:
                cfg, res = tee(f)
                # set 1 line above:
                for i in range(1):
                    next(cfg)
                for c, r in zip(cfg, res):
                    if "NOT Converted." in c:
                        not_converted_list.append(r)

    not_converted_list_single = set(not_converted_list)
    print(f'''
        Not converted: {str(len(not_converted_list))}
        Not converted list set: {str(len(not_converted_list_single))}
        ''')
    with open(r'../list.txt', 'w') as fp:
        for item in not_converted_list_single:
            # write each item on a new line
            fp.write("%s\n" % item)
        print('Done')

def parseList(packages):
    SPDXConverted = []
    os.chdir("/src/LCV/LCVlib")
    for license in packages:
        if license is not None and not license == "" and not license == "404":
            if "same as" in license:
                strippedName = []
                strippedName = license.split()
                for name in strippedName:
                    if name == "same" or name == "as":
                        strippedName.remove(name)
                licenseName = ''.join(strippedName)
                licenseName = licenseName.lower()
                license = RetrievePypiLicenseInformationPackage(licenseName)
            # trying to catch long license declarations
            # TODO append some special output to indicate that here the margin of error is higher
            if "www." in license:
                TryingConversion = ConvertToSPDX(license)
                print("XXXXXXXXXXXXXXXX")
                print(TryingConversion)
                license = TryingConversion
            for char in list_of_parenthesis:
                if char in license:
                    license = RemoveParenthesisAndSpecialChars(license)
            possibleSPDX = license
            IsSPDX = APICallIsAnSPDX(license)
            if IsSPDX:
                IsSPDX = "Pypi provided an SPDX id."
                SPDXConverted.append(possibleSPDX)
            else:
                if "+" in license:
                    licenseMod = license.replace("+", "%2B")
                    possibleSPDX = APICallConvertToSPDX(licenseMod)
                else:
                    possibleSPDX = APICallConvertToSPDX(license)
                if possibleSPDX is not None:
                    IsSPDX = APICallIsAnSPDX(possibleSPDX)
                    if IsSPDX:
                        IsSPDX = "Converted."
                        SPDXConverted.append(possibleSPDX)
                    if not IsSPDX:
                        IsSPDX = "NOT Converted."
        time.sleep(2)
    print("SPDXConverted list size:")
    print(len(SPDXConverted))

    with open(r'list_converted.txt', 'w') as fp:
        for item in SPDXConverted:
            # write each item on a new line
            fp.write("%s\n" % item)
        print('Done')


def readList():
    packages = []
    with open(r'../list.txt', 'r') as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            packages.append(x)
    packages = set(packages)
    return packages

def main():
    # provides statistical information parsing the logs
    scandir()
    # retrieves license name not converted.
    not_converted_list()

    # parse the txt generated with license name not converted to a list
    packages = readList()
    #print(str(packages))
    # perform queries upon LCV for SPDXConversion
    parseList(packages)

if __name__ == "__main__":
    main()
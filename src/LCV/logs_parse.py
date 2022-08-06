import time
import re
import os
from SPDXIdMapping import StaticMappingList,IsAnSPDX,StaticMapping,DynamicMapping,IsInAliases,ConvertToSPDX

#import pandas as pd

#counters
import requests as requests

txt_list = []
base_dir = ("/home/michelescarlato/gitrepo/LCV-CM/src/LCV/collectingPypiLicenses/output/already_parsed")


def RetrievePypiLicenseInformationPackage(packageName):
    #Example: GET https://pypi.org/pypi/standalone/1.0.1/json
    response = requests.get("https://pypi.org/pypi/"+packageName+"/json")
    if response.status_code == 200:
        jsonResponse=response.json()
        license=(jsonResponse["info"]["license"])
        return license
    else:
        license = "404"
        output=packageName+", 404 - page not found"
        print(output)
        appendToFile(output)
        return license

def APICallConvertToSPDX(license):
    #response = requests.get("https://lima.ewi.tudelft.nl/lcv/ConvertToSPDX?VerboseLicense="+license)
    response = requests.get("http://0.0.0.0:3251/ConvertToSPDX?VerboseLicense="+license)
    jsonResponse=response.json()
    #print(jsonResponse)
    return jsonResponse

def APICallIsAnSPDX(license):
    #response = requests.get("https://lima.ewi.tudelft.nl/lcv/IsAnSPDX?SPDXid="+license)
    response = requests.get("http://0.0.0.0:3251/IsAnSPDX?SPDXid="+license)
    jsonResponse=response.json()
    #print(jsonResponse)
    return jsonResponse

def appendToFile(license):
    with open("collectingPypiLicenses/output/whole-pypi-package-list-ConvertToSPDX"+str(startLine)+"-"+str(endLine)+".txt", "a+") as file_object:
    #with open("collectingPypiLicenses/output/Re-factoring-testing.txt", "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(license)



def scandir():
    not_converted = 0
    converted = 0
    already_SPDX = 0
    none_license = 0
    not_found = 0
    not_converted_list = []
    for dirpath, dirnames, filename in os.walk(base_dir):
        for filename in filename:
            # create full path
            txtfile_full_path = os.path.join(dirpath, filename)
            with open(txtfile_full_path) as f:
                lineCounter = 0
                print(filename)
                lines = f.readlines()
                #current_line = f.readline()
                for line in lines:
                    previous_line = lineCounter - 1
                    if "NOT Converted." in line:
                        # stores the not converted license names in a list
                        not_converted_list.append(lines[previous_line])
                        not_converted += 1
                        lineCounter += 1
                        pass
                    if "Converted." in line:
                        converted += 1
                        lineCounter += 1
                        pass
                    if "Pypi provided an SPDX id." in line:
                        already_SPDX += 1
                        lineCounter += 1
                        pass
                    if "detected pypi license: None" in line:
                        none_license += 1
                        lineCounter += 1
                        pass
                    if "404 - page not found" in line:
                        not_found += 1
                        lineCounter += 1
                        pass

        not_converted_list_clean = list(set(not_converted_list))
        total_packages = not_converted + converted + already_SPDX + none_license + not_found
        print(f'''
        Not converted: {not_converted}
        Converted : {converted}
        Already SPDX : {already_SPDX}
        None license : {none_license}
        404 not found : {not_found}
        not_converted_list size: {str(len(not_converted_list))}        
        not_converted_list without duplicates size: {str(len(not_converted_list_clean))}
        Total packages analyzed: {total_packages}
        ''')


def main():
    scandir()
    for package in not_converted_list_clean:
        output = None
        license = RetrievePypiLicenseInformationPackage(package)
        if license is not None and not license == "" and not license == "404":
            if "same as" in license:
                strippedName = []
                strippedName = license.split()
                for name in strippedName:
                    if name is "same" or name is "as":
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
                    if not IsSPDX:
                        IsSPDX = "NOT Converted."
            line_number = 0
            # add line number
            with open('whole_pypi_package_list.txt', 'r') as g:
                for line in g:
                    line_number += 1
                    if re.search(rf"\b(?=\w){package}\b(?!\w)", line, re.IGNORECASE):
                        output = str(line_number) + " " + package + ",\n" + str(license) + ",\n" + str(
                            possibleSPDX) + ",\n" + str(IsSPDX)
                        print(output)
            if output is None:
                output = package + ",\n" + str(license) + ",\n" + str(possibleSPDX) + ",\n" + str(IsSPDX)
                print(output)
            appendToFile(output)
        if license is None or license == "":
            output = package + ", detected pypi license: None"
            print(output)
            appendToFile(output)
        if license == "404":
            print("404 - page not found")
        time.sleep(5)

if __name__ == "__main__":
    main()
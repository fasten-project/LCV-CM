
import re
import os
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
    for dirpath, dirnames, filename in os.walk(base_dir):
        for filename in filename:
            # create full path
            txtfile_full_path = os.path.join(dirpath, filename)
            with open(txtfile_full_path) as f:
                print(filename)
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


def main():
    scandir()

if __name__ == "__main__":
    main()
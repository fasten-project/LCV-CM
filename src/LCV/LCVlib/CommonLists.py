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
LicenseLetterVersion = ["b","c"]
literalVersions = ["one","two","three","four","five"]

list_of_parenthesis=['(', ')','[', ']',';', ',','"','\'']

DynamicMappingKeywordsList = [
    "2010", "2014", "academic", "affero","agpl", "apache", "attribution","beer"
    "berkeley", "bsd", "bzip","cecill" ,"classpath", "clear", "cmu", "cpe", "commons", "creative",
    "database", "distribution", "eclipse", "epl", "eupl", "european",
    "exception","expat", "general", "gpl", "gnu", "ibm", "later", "lesser","lgpl", "libpng", "library", "license", "miros","microsoft", "mit", "mozilla", "modification", "mpi",
    "mpl", "ntp", "new", "nuclear", "national", "only", "open", "openssl", "patent", "psf","psfl", "python",
    "png", "power", "powerpc", "public", "permissive", "qhull", "reciprocal", "shortened","simplified","software", "tiff", "uc", "universal","unlicense",
    "upl", "views", "warranty", "zlib", "zero","AFL", "AGPL", "Apache", "Artistic", "BSD", "BSL", "bzip2", "CC0", "CDDL", "CPE", "CPL", "curl",
    "EFL", "EPL", "EUPL", "FTL", "GPL", "HPND", "IBM", "ICU", "IJG", "IPL", "ISC", "LGPL", "Libpng", "libtiff", "MirOS", "MIT", "CMU", "MPL",
    "MS", "NBPL", "NTP", "OpenSSL", "OSL", "Python", "Qhull", "RPL", "SunPro", "Unicode",
    "UPL", "WTFPL", "X11", "XFree86", "Zlib", "zlib-acknowledgement"]

NumberDict = {
  "one": "1",
  "two": "2",
  "three": "3",
  "four": "4",
  "five": "5"
}

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
    "a", "2007" ,"2010", "2014", "academic", "affero", "agpl", "apache", "attribution","beer"
    "berkeley", "bsd", "bzip", "cecill", "classpath", "clear", "cmu", "cpe", "commons", "creative",
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

DynamicMappingKeywordsDict = {
    "bsd": {
        "2.0": "BSD-2-Clause",
        "3.0": "BSD-3-Clause",
        "attribution": "BSD-3-Clause-Attribution",
        "clear": "BSD-3-Clause-Clear",
        "database" : "Sleepycat",
        "military": "BSD-3-Clause-No-Military-License",
        "modification": "BSD-3-Clause-Modification",
        "national": "BSD-3-Clause-LBNL",
        "new": "BSD-3-Clause",
        "nuclear": {
                    "2014": "BSD-3-Clause-No-Nuclear-License-2014",
                    "warranty": "BSD-3-Clause-No-Nuclear-Warranty",
                    "": "BSD-3-Clause-No-Nuclear-License", #TODO how to set a default value for a not matching key.
                },
        "open": {"mpi": "BSD-3-Clause-Open-MPI"},
        "patent": "BSD-2-Clause-Patent",
        "shortened": "BSD-4-Clause-Shortened",
        "simplified": "BSD-2-Clause",
        "uc": "BSD-4-Clause-UC",
        "views": "BSD-2-Clause-Views",
    },
    "academic": "AFL",
    "bzip" : {
            "2007" : "bzip2-1.0.5",
            "1.0.5" : "bzip2-1.0.5",
            "2010" : "bzip2-1.0.6",
            "1.0.6" : "bzip2-1.0.6",
    },
    "apache" : {
            "1.0" : "Apache-1.0",
            "2.0" : "Apache-2.0"
    },
    "beer" : "Beerware",
    "cecill": {
        "b": "CECILL-B",
        "c": "CECILL-C",
        "1.0": "CECILL-1.0",
        "1.1": "CECILL-1.1",
        "2.0": "CECILL-2.0",
        "2.1": "CECILL-2.1",
    },
    "distribution": {
        "1.0" : "CDDL-1.0",
        "1.1" : "CDDL-1.1",
    },
    "powerpc" : "IBM-pibs",
    "power" : "IBM-pibs",
    "tiff" : "libtiff",
    "miros" : "MirOS",
    "mit" : "MIT",
    "cmu": "MIT-CMU",
    "classpath": "GPL-2.0-with-classpath-exception",
    "expat": "MIT",
    "ibm": "IPL-1.0",
    "libpng": {
        "2.0": "libpng-2.0",
    },

}

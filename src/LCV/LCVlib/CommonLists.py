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
    "berkeley", "bsd", "bzip", "cc", "cecill", "classpath", "clear", "cmu", "cpe", "commons", "creative",
    "database", "distribution", "eclipse", "epl", "eupl", "european",
    "exception","expat", "general", "gpl", "gnu", "ibm", "iscl", "later", "lesser","lgpl", "libpng",
    "library", "license", "miros","microsoft", "mit", "mozilla", "modification", "mpi",
    "mpl", "ntp", "new", "nuclear", "national", "only", "open", "openssl", "patent","pddc", "psf","psfl", "python",
    "png", "power", "powerpc", "public", "permissive", "qhull", "reciprocal", "shortened","simplified",
    "software", "tiff", "uc", "universal","unlicense","upl", "views", "warranty", "zlib", "zero","AFL",
    "AGPL", "Apache", "Artistic", "BSD", "BSL", "bzip2", "CC0", "CDDL", "CPE", "CPL", "curl",
    "EFL", "EPL", "EUPL", "FTL", "GPL", "HPND", "IBM", "ICU", "IJG", "IPL", "ISC", "LGPL", "Libpng",
    "libtiff", "MirOS", "MIT", "CMU", "MPL", "MS", "NBPL", "NTP", "OpenSSL", "OSL", "Python",
    "Qhull", "RPL", "SunPro", "Unicode",
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
        "database": "Sleepycat",
        "sleepycat": "Sleepycat",
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
    "cc":{
        "by":{
            "1.0": "CC-BY-1.0",
            "2.0": "CC-BY-2.0",
            "2.5": "CC-BY-2.5",
            "au": "CC-BY-2.5-AU",
            "at" : "CC-BY-3.0-AT",
            "de" : "CC-BY-3.0-DE",
            "nl" : "CC-BY-3.0-NL",
            "us" : "CC-BY-3.0-US",
            "3.0": "CC-BY-3.0",
            "4.0": "CC-BY-4.0",
            "nc":{
                "1.0": "CC-BY-NC-1.0",
                "2.0": "CC-BY-NC-2.0",
                "2.5": "CC-BY-NC-2.5",
                "de": "CC-BY-NC-3.0-DE",
                "3.0": "CC-BY-NC-3.0",
                "4.0": "CC-BY-NC-4.0",
                "nd":{
                    "1.0": "CC-BY-NC-ND-1.0",
                    "2.0": "CC-BY-NC-ND-2.0",
                    "2.5": "CC-BY-NC-ND-2.5",
                    "de": "CC-BY-NC-ND-3.0-DE",
                    "IGO": "CC-BY-NC-ND-3.0-IGO",
                    "3.0": "CC-BY-NC-ND-3.0",
                    "4.0": "CC-BY-NC-ND-4.0",
                },
                "sa":{
                    "1.0": "CC-BY-NC-SA-1.0",
                    "2.0": "CC-BY-NC-SA-2.0",
                    "fr": "CC-BY-NC-SA-2.0-FR",
                    "uk": "CC-BY-NC-SA-2.0-UK",
                    "2.5": "CC-BY-NC-SA-2.5",
                    "3.0": "CC-BY-NC-SA-3.0",
                    "de" : "CC-BY-NC-SA-3.0-DE",
                    "igo" : "CC-BY-NC-SA-3.0-IGO",
                    "4.0" : "CC-BY-NC-SA-4.0",
                },
            },
            "nd":{
                "1.0": "CC-BY-ND-1.0",
                "2.0": "CC-BY-ND-2.0",
                "2.5": "CC-BY-ND-2.5",
                "3.0": "CC-BY-ND-3.0",
                "de" : "CC-BY-ND-3.0-DE",
                "4.0": "CC-BY-ND-4.0",
            },
            "sa":{
                "1.0": "CC-BY-SA-1.0",
                "2.0": "CC-BY-SA-2.0",
                "uk": "CC-BY-SA-2.0-UK",
                "jp": "CC-BY-SA-2.1-JP",
                "2.1": "CC-BY-SA-2.1-JP",
                "2.5": "CC-BY-SA-2.5",
                "3.0": "CC-BY-SA-3.0",
                "at" : "CC-BY-SA-3.0-AT",
                "de" : "CC-BY-SA-3.0-DE",
                "4.0" : "CC-BY-SA-4.0",
            },
        },
        "pddc":"CC-PDDC",
    },
    "cc0": "cc0-1.0",
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
        "zlib": "Zlib",
    },
    "eclipse": {
        "1.0": "EPL-1.0",
        "2.0": "EPL-2.0",
    },
    "european": {
        "1.0": "EUPL-1.0",
        "1.1": "EUPL-1.1"
    },
    "mozilla": {
        "1.0": "MPL-1.0",
        "1.1": "MPL-1.1",
        "2.0": "MPL-2.0",
        "exception": "MPL-2.0-no-copyleft-exception",
    },
    "ntp": {

    }


}

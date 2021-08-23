if len(MappedKeywords):
    '''if "later" in MappedKeywords:
        orLater = True
    if "only" in MappedKeywords:
        only = True'''
    SubDict = DynamicMappingKeywordsDict
    for key in MappedKeywords:
        print("Searching for:"+key)
        if key in SubDict:
            NewDict = SubDict.get(key)
            MappedKeywords.remove(key)
            if IsAnSPDX(str(NewDict)):
                return str(NewDict)
            for key in MappedKeywords:
                if key in NewDict:
                    SecondNewDict = NewDict.get(key)
                    MappedKeywords.remove(key)
                    if IsAnSPDX(str(SecondNewDict)):
                        return str(SecondNewDict)
                    for key in MappedKeywords:
                        if key in SecondNewDict:
                            ThirdNewDict = SecondNewDict.get(key)
                            MappedKeywords.remove(key)
                            if IsAnSPDX(str(ThirdNewDict)):
                                return str(ThirdNewDict)

if len(MappedKeywords):
    '''if "later" in MappedKeywords:
        orLater = True
    if "only" in MappedKeywords:
        only = True'''
    SubDict = DynamicMappingKeywordsDict
    for key in MappedKeywords:
        print("Searching for:"+key)
        #1st nested level
        if key in SubDict:
            MappedKeywords.remove(key)
            SubDict = SubDict.get(key)
            if IsAnSPDX(str(SubDict)):
                return str(SubDict)
            #2nd nested level
            for key in MappedKeywords:
                if key in SubDict:
                    MappedKeywords.remove(key)
                    SubDict = SubDict.get(key)
                    if IsAnSPDX(str(SubDict)):
                        return str(SubDict)
                    #3rd nested level
                    for key in MappedKeywords:
                        if key in SubDict:
                            MappedKeywords.remove(key)
                            SubDict = SubDict.get(key)
                            if IsAnSPDX(str(SubDict)):
                                return str(SubDict)

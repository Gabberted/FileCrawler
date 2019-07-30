import vars
import time
import os

def readHTMLFile(strFile):
    strHTML=""
    try:
        print("Here we need to read the file")
        print("Opening file: " + strFile)
        days_file = open(strFile,'r')
        strHTML = days_file.read()
        days_file.close()

    except:
        print("Error reading file")
        days_file.close()
        #print(str(Error))
    finally:

        return strHTML

def writeTxtFile():
    try:
        fh = open("testfile", "w")
        try:
            fh.write("This is my test file for exception handling!!")
        finally:
            print ("Going to close the file")
            fh.close()
    except IOError:
        print ("Error: can\'t find file or read data")

def CreateTableContent(list):
    print("Generating table content")
    strRet="<tr>"
    iCnt=0
    print(list)
    time.sleep(15)
    for item in list.split("@"):
        #print("Item: " + item)
        for strValue in item.split("#"):
            strRet=strRet + "<td>" + str(iCnt) + "</td>"
            strRet=strRet + "<td>" + str(item.split("#")[1]) + "</td>"
            strSplit=item.split("/")
            #print(count(strSplit[0])
            strRet=strRet + "<td>" + str(item.split("#")[0]) + "</td>"
            strRet=strRet + "<td>"  + str(item.split("#")[2]) + "</td>"
            strRet=strRet + "<td>" + str(item.split("#")[3]) + "</td>"
            strRet=strRet + "</tr><tr>"
            iCnt=iCnt+1
            #print(item)

    strRet=strRet + "</tr>"
    return strRet

def getFileExtention(strFileName):
    try:
        print("Entering getFileExtention with: " + str(strFileName))
        strSplit=strFileName.split('.')
        print(strSplit)
        print("Extention found: " + str(strSplit[len(strSplit)-1]))
        return strSplit[1]
    except:
        print ("Error while executing getFileExtention")

def doStuff(strPath):
    strHTML= readHTMLFile(strPath)
    return strHTML

def getFooter():
    strFooterPath=os.path.dirname(__file__) + vars._FooterFile
    print("getFooter: " + strFooterPath)
    return readHTMLFile(strFooterPath)

def getStyleSheet():
    strStyleSheet=os.path.dirname(__file__).replace("app","") + vars._StyleSheet
    print("strStyleSheet: " + strStyleSheet)
    return readHTMLFile(strStyleSheet)

def getCrawlBtn():
        strStyleSheet=os.path.dirname(__file__).replace("app","") + vars._btnCrawlFolder
        print("getCrawlBtn: " + strStyleSheet)
        return readHTMLFile(strStyleSheet)


def getFooterContent(strFooterPath):
    if not strFooterPath:
        strFooterPath=getFooter()

    print("Calling readHTMLFile on " +str(strFooterPath))
    return readHTMLFile(strFooterPath)

def getAllMakeUpDone():
    strFooterPath=os.path.dirname(__file__).replace("app","") + vars._FooterFile
    strFOOTERHTML= getFooterContent(strFooterPath)
    strStyleSheetHTML= getStyleSheet()
    btnCrawlHTML= getCrawlBtn()

    return strFOOTERHTML, strStyleSheetHTML, btnCrawlHTML

def getTemplate(strPath):
    strPath=os.path.dirname(__file__).replace("app","") + strPath
    strFooterHTML, strStyleSheet, btnCrawlHTML =getAllMakeUpDone()
    print("opening:" + str(strPath))
    strHTML= readHTMLFile(strPath).replace("%FOOTER%",strFooterHTML).replace("%STYLE%",strStyleSheet).replace("%BTNCRAWL%",btnCrawlHTML)

    return strHTML

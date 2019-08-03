import vars
import time
import os
import app.db as db

def readHTMLFile(strFile):
    strHTML=""
    try:
        print("readHTMLFile")
        print("Opening file: " + strFile)

        days_file = open(strFile,'r')
        strHTML = days_file.read()
        days_file.close()
    except IOError:
        print("Could not open file! Please close the file: " + str(strFile))
    except:
        print("Error reading file")
        days_file.close()
        #print(str(Error))
    finally:
        #days_file.close()
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
    time.sleep(0.1)
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

def CreateTableContentFromDB(strQuery):
    print("Generating table content")
    rows=db.executeQueryReturnRows(strQuery)
    print("Rows: " + str(len(rows)))
    strRet="<TABLE border=1><tr>"
    iCnt=0
    time.sleep(0.1)
    for row in rows:
        strRet=strRet + "<tr>"
        for cell in row:
            strRet=strRet + "<td>" + str(cell) + "</td>"
        strRet=strRet + "</tr>"
    strRet=strRet + "</tr></TABLE>"
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
    strFooterPath=os.path.dirname(__file__).replace("app","")  + vars._FooterFile
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
    print("Building page")
    strFooterPath=os.path.dirname(__file__).replace("app","") + vars._FooterFile
    print("With footer:" + str(strFooterPath))
    strFOOTERHTML= getFooterContent(strFooterPath)
    print("Fetching stylesheet")
    strStyleSheetHTML= getStyleSheet()
    print("Crawl button")
    btnCrawlHTML= getCrawlBtn()
    print("Returning from getAllMakeUpDone()")
    return strFOOTERHTML, strStyleSheetHTML, btnCrawlHTML

def getTemplate(strPath):
    strFooterHTML, strStyleSheet, btnCrawlHTML =getAllMakeUpDone()

    #strPath=os.path.dirname(__file__).replace("app","") + vars._FooterFile

    print("Fetching template:" + str(strPath))
    strHTML= readHTMLFile(strPath).replace("%FOOTER%",strFooterHTML).replace("%STYLE%",strStyleSheet).replace("%BTNCRAWL%",btnCrawlHTML)
    print(strHTML)
    return strHTML

def makeListFromHTMLTable(HTMLTable):
    strHTML = HTMLTable.replace("<TABLE>","").replace("</TABLE>","").replace("<tr>","").replace("<td>","").replace("</td>","").replace("</tr>",",")
    return strHTML.split(',')

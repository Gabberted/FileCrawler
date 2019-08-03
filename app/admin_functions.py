import FrameWork.debug as debug
from sqlite3 import Error
import os
import app.db as db
import FrameWork.debug as debug
import vars
import app.MiddleWare as mw

strFooterPath=os.path.dirname(__file__) + vars._FooterFile

def main():
    #strPath=os.path.dirname(__file__) + vars._indexFile
    strPath=os.path.dirname(__file__).replace("app","") + vars._WelcomeFile
    debug.debugPrint("PATH FOUND: " + strPath)

    #strFooterPath=os.path.dirname(__file__) + vars._FooterFile
    print("Generated FooterFile: " + strFooterPath)

    #print(strPath)
    strFooter, strStyle,btnCrawlHTML=mw.getAllMakeUpDone()
    return mw.readHTMLFile(strPath).replace("%FOOTER%", str(strFooter)).replace("%STYLE%", str(strStyle)).replace("%BTNCRAWL%",str(btnCrawlHTML))
    return strRet

def admin():
    strPath=os.path.dirname(__file__).replace("app","") + vars._AdminFile
    debug.debugPrint("AdminFile: " + str(strPath))
    strFooter, strStyle,btnCrawlHTML=mw.getAllMakeUpDone()
    return mw.readHTMLFile(strPath).replace("%FOOTER%", str(strFooter)).replace("%STYLE%", str(strStyle)).replace("%BTNCRAWL%",str(btnCrawlHTML))

def crawler():
    retval= crawl.Crawl(vars.rootdir)
    strPath=os.path.dirname(__file__) + vars._CrawlFile
    debug.debugPrint("AdminFile: " + str(strPath))
    strFooter, strStyle, btnCrawlHTML=mw.getAllMakeUpDone()
    retval="Done"
    return mw.readHTMLFile(strPath).replace("%FOOTER%", str(strFooter)).replace("%STYLE%", str(strStyle)).replace("%MESSAGE%", str(retval)).replace("%BTNCRAWL%",str(btnCrawlHTML))

def showfiles():
    print("showing")
    retVal= db.ShowAllFiles()
    #retVal=retVal.replace("@","<br>")
    #retVal= vars.strHTMLHeader + retVal
    #debug.debugPrint(retVal)
    strPath=os.path.dirname(__file__) + vars._indexFile
    strContent=mw.CreateTableContent(retVal)
    print("Content: " + strContent)
    #tm.SleepSeconds(5)

    strFooter, strStyle,btnCrawlHTML=mw.getAllMakeUpDone()
    strRet = str(mw.readHTMLFile(strPath).replace("%tbl_cntnt%",strContent))
    strRet = strRet.replace("%FOOTER%", str(strFooter)).replace("%STYLE%", str(strStyle)).replace("%BTNCRAWL%",str(btnCrawlHTML))
    retVal = strRet

    return retVal


def whipefiles():
    print("Clearing out database")
    strQuery="delete from FileNames"
    retVal= db.executeQuery(strQuery)

    strPath=os.path.dirname(__file__) + vars._DoneFile
    return mw.getTemplate(strPath).replace("%MESSAGE%", str(retVal))

def initsystem():
    strQuery="DROP TABLE FileNames;"
    print("Dropping table FileNames")
    retVal= db.executeQuery(strQuery)

    strQuery="DROP TABLE Extentions;"
    print("Dropping table Extentions")
    retVal= db.executeQuery(strQuery)
    db.sql_table()
    return "Database Created"

import FrameWork.debug as debug
from sqlite3 import Error
import os
import app.db as db
import FrameWork.debug as debug
import vars
import app.MiddleWare as mw

strFooterPath=os.path.dirname(__file__) + vars._FooterFile

def genExtentions():
    print("Generating Extentions from FileNames stored in DB")
    strQuery="select distinct Name from FileNames limit 100"
    #strRet= db.executeQuery(strQuery)
    print("Creating Table")
    strContent=mw.CreateTableContentFromDB(strQuery)
    print(strContent)
    List=mw.makeListFromHTMLTable(strContent)
    print("Looping through list")
    for strExtention in List:
        strExt=mw.getFileExtention(strExtention)
        print("Probing: " + (strExtention) + " -> " + str(strExt))
        if db.ItemAlreadyInDb(strExt, "Extentions", "Ext")==0:

            print("Extention added: " + str(strExt))
            strQuery="insert into Extentions(Ext, count)values('" + str(strExt) + "','1')"
            strRet= db.executeQuery(strQuery)
            print("Extention added: " + str(strExt))
        else:
            print("Extention not added, already stored")

    return strContent

def showExtentions():
    print("Showing Extentions stored DB")
    strQuery="select * from Extentions"
    #strRet= db.executeQuery(strQuery)
    print("Creating Table")
    strContent=mw.CreateTableContentFromDB(strQuery)
    print(strContent)
    return str(strContent)


def clearExtentions():
    print("Clearing Extentions DB")
    print("whiping old data")
    strQuery="delete from Extentions"
    strRet= db.executeQuery(strQuery)
    return str(strRet)


def cleanExtentions():
    print("Collecting Extentions")
    strQuery="Select distinct Ext from Extentions"
    rows = db.returnRows(strQuery)
    List=[]
    for row in rows:
            List.append(str(row[0]))
            print("Appending" + str(row[0]))

    print("whiping old data")
    strQuery="delete from Extentions"
    db.executeQuery(strQuery)

    print("Refreshing data")
    for item in List:
        strQuery="insert into Extentions(Ext)values('" + str(item) + "')"
        db.executeQuery(strQuery)
        print("Ext updated " + str(item))

    return showInfo()

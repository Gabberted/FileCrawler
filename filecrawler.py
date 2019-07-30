from flask import Flask
import app.db as db
import FrameWork.debug as debug
import FrameWork.TimeFunctions as tm
import app.MiddleWare as mw
import app.crawls as crawl
import vars
import os



#functions
app = Flask(__name__)
print(str(app.route))

#local variables
strFooterPath=os.path.dirname(__file__) + vars._FooterFile

#routing
@app.route("/")
def main():
    #strPath=os.path.dirname(__file__) + vars._indexFile
    strPath=os.path.dirname(__file__) + vars._WelcomeFile
    debug.debugPrint("PATH FOUND: " + strPath)

    #strFooterPath=os.path.dirname(__file__) + vars._FooterFile
    print("Generated FooterFile: " + strFooterPath)

    #print(strPath)
    strFooter, strStyle=mw.getAllMakeUpDone()
    return mw.readHTMLFile(strPath).replace("%FOOTER%", str(strFooter)).replace("%STYLE%", str(strStyle))
    return strRet

@app.route("/admin")
def admin():
    strPath=os.path.dirname(__file__) + vars._AdminFile
    debug.debugPrint("AdminFile: " + str(strPath))
    strFooter, strStyle=mw.getAllMakeUpDone()
    return mw.readHTMLFile(strPath).replace("%FOOTER%", str(strFooter)).replace("%STYLE%", str(strStyle))


@app.route("/crawl")
def crawler():
	retval= crawl.Crawl(vars.rootdir)
	return retval[1]


@app.route("/show")
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

    strFooter, strStyle=mw.getAllMakeUpDone()
    strRet = str(mw.readHTMLFile(strPath).replace("%tbl_cntnt%",strContent))
    strRet = strRet.replace("%FOOTER%", str(strFooter)).replace("%STYLE%", str(strStyle))
    retVal = strRet

    return retVal


@app.route("/info")
def showInfo():
    strInfo, strDistinct, strMP3, strWav, strflv, strAvi =db.showInfo()
    strBMP, strJPG, strpng, strTiff = db.showPictureInfo()
    strDOC , strDOCX, strODT, strTXT = db.showDocumentInfo()
    strPY,strC,strBAS,strH, strCPP, strPY_L,strC_L,strBAS_L,strH_L,strCPP_L  = db.showProjectInfo()
    strList=""
    #strList=db.getALlStoredFileExtentions()
    print("Collecting summery")
    #strSummery=db.getOverAllSummery()
    strSummery=""
    strPath=os.path.dirname(__file__) + vars._infoFile
    strFooterPath=os.path.dirname(__file__) + vars._FooterFile

    #get the footer data
    strFooterHTML= mw.readHTMLFile(strFooterPath)

    strHTML= mw.readHTMLFile(strPath).replace("%info%",strInfo).replace("%info2%",strDistinct).replace("%MP3%",strMP3).replace("%WAV%",strWav).replace("%summery%",strSummery).replace("%avi%",strAvi).replace("%flv%",strflv)
    strHTML=strHTML.replace("%BMP%",strBMP).replace("%JPG%",strJPG).replace("%PNG%",strpng).replace("%TIFF%",strTiff).replace("%DOC%",strDOC).replace("%DOCX%",strDOCX).replace("%ODT%",strODT).replace("%TXT%",strTXT)
    strHTML=strHTML.replace("%T_PY%",strPY).replace("%T_C%",strC).replace("%T_BAS%",strBAS).replace("%T_h%",strH)
    strHTML=strHTML.replace("%T_PY_L%",strPY_L).replace("%T_C_L%",strC_L).replace("%T_BAS_L%",strBAS_L).replace("%T_h_L%",strH_L).replace("%T_CPP_L%",strCPP_L).replace("%T_CPP%",strCPP)
    strFooter, strStyle=mw.getAllMakeUpDone()
    strHTML = strHTML.replace("%FOOTER%", str(strFooter)).replace("%STYLE%", str(strStyle))
    return strHTML

@app.route("/whipe")
def whipefiles():
    print("Clearing out database")
    strQuery="delete from FileNames"
    retVal= db.executeQuery(strQuery)

    strPath=os.path.dirname(__file__) + vars._DoneFile
    return mw.getTemplate(strPath).replace("%MESSAGE%", str(retVal))

@app.route("/nothing")
def donothing():
	return "nothing"


@app.route("/init")
def initsystem():
    strQuery="DROP TABLE FileNames;"
    print("Dropping table FileNames")
    retVal= db.executeQuery(strQuery)

    strQuery="DROP TABLE Extentions;"
    print("Dropping table Extentions")
    retVal= db.executeQuery(strQuery)
    db.sql_table()
    return "Database Created"

@app.route('/test1')
def dostuff():
    debug.debugPrint("Testing")
    strFooterPath=os.path.dirname(__file__) + vars._FooterFile
    print("Generated FooterFile: " + strFooterPath)
    return mw.doStuff(strFooterPath)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

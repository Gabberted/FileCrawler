from flask import Flask
from flask import request
import app.db as db
import app.admin_functions as ad
import app.extention_functions as ext
import app.pol_functions as pol
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
    return ad.main()

@app.route("/admin")
def admin():
    return ad.admin()


@app.route("/crawl")
def crawler():
    return ad.crawler()

@app.route("/show")
def showfiles():
    return ad.showfiles()

@app.route("/genExtentions")
def genExtentions():
    return ext.genExtentions()

@app.route("/showExtentions")
def showExtentions():
    return ext.showExtentions()

@app.route("/clearExtentions")
def clearExtentions():
    return ext.clearExtentions()

@app.route("/cleanExtentions")
def cleanExtentions():
    return ext.cleanExtentions()

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
    strFooter, strStyle,btnCrawlHTML=mw.getAllMakeUpDone()
    strHTML = strHTML.replace("%FOOTER%", str(strFooter)).replace("%STYLE%", str(strStyle)).replace("%BTNCRAWL%",str(btnCrawlHTML))
    return strHTML

@app.route("/whipe")
def whipefiles():
    return ad.whipefiles()

@app.route("/nothing")
def donothing():
	return "nothing"


@app.route("/init")
def initsystem():
    return ad.initsystem()

@app.route('/test1')
def dostuff():
    debug.debugPrint("Testing")
    #strFooterPath=os.path.dirname(__file__) + vars._TestFile
    #print("Generated Test1: " + strFooterPath)
    #return mw.doStuff(strFooterPath)
    #strQuery="insert into Extentions(Ext, count)values('" + str(strExt) + "','1')"
    strQuery="insert into Extentions(Ext, count)values('gif','1')"

    strRet= db.executeQuery(strQuery)

    return str(strRet)

@app.route("/LendingRates")
def LendingRates():
    return pol.LendingRates()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

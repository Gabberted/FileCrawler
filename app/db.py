import sqlite3
from sqlite3 import Error
import datetime
import vars
import FrameWork.debug as debug
import app.MiddleWare as mw
import os


debug=True

con = sqlite3.connect(vars.strDbName, check_same_thread=False)
con2 = sqlite3.connect(vars.strDbName, check_same_thread=False)

#db stuff
def debugPrint(strText):
    if(debug==True):
        print("DEBUG: " + str(strText))

def storeSingeFile(FileName):
    debugPrint("Entering storeSingleFile")
    extList=[]
    try:
        with sqlite3.connect("file.db") as con2:
            cur = con2.cursor()
            debugPrint("Executing SingleFile Query")
            iFileCounter=0
            #FileName = FileName.replace("[","").replace("'","").replace("]","").strip().split(",")
            FileName = returnFilePathToStore(str(FileName))
            #lets check if the file is already in the db,
            #if so we dont need to add it.
            debugPrint(FileName)
            debugPrint("Looking up file!")
            try:
                boFileStored=False
                boFileStored = FileAlreadyStored(FileName)
            except Error:
                debugPrint("Error looking up Filestored")
                debugPrint(str(Error))
            finally:
                if boFileStored != True:
                    debugPrint("File Not found so adding!")
                    try:
                        Date= os.path.getmtime(FileName.strip())
                        Size= os.path.getsize(FileName.strip())
                    except:
                        Date=str(datetime.datetime.now())
                        Size=0
                    debugPrint(Date)
                    strQuery="insert into FileNames(name, path, date, size)values('@filename','@filepath','@filedate','@n')"
                    FileName = returnFilePathToStore(str(FileName))
                    strQuery=strQuery.replace('@filepath',returnFilePathToStore(FileName))
                    FileName=FileName.split("/")
                    strQuery=strQuery.replace('@filename',FileName[len(FileName)-1])

                    strQuery=strQuery.replace('@filedate',str(Date))
                    strQuery=strQuery.replace('@n',str(Size))

                    print(strQuery)

                    curInject = con2.cursor()
                    curInject.execute(strQuery)
                    print("Insert File Query Executed")

                    #now lets see if we need to update the extention db
                    iLenght=len(FileName)-1
                    print("FileName:" + str(FileName))
                    print("Lenght found:" + str(iLenght))
                    strFileName=FileName[iLenght];
                    #strFileName=strFileName.split('.')[iLenght-1]
                    print("Filename:" + str(strFileName))

                    strExtention=mw.getFileExtention(str(strFileName))
                    if not strExtention in extList:
                        extList.append(str(strExtention))
                        strQuery="insert into Extentions(Ext, count)values('@strExt','1')"
                        strQuery=strQuery.replace("@strExt", str(strExtention))
                        curInject.execute(strQuery)
                        print("Insert Extention Executed")
                else:
                    debugPrint("FileName not stored: " + str(FileName))

    finally:
        print("Added: " + str(FileName))

def StoreFileList(FileList):
    try:
        with sqlite3.connect("file.db") as con2:
            cur = con2.cursor()
            debugPrint("Executing Query")
            iFileCounter=0
            for FileName in FileList.replace("[","").replace("'","").replace("]","").strip().split(","):
                #lets check if the file is already in the db,
                #if so we dont need to add it.
                debugPrint(FileName)
                if FileAlreadyStored(FileName) == False:
                    try:
                        Date= os.path.getmtime(FileName.strip())
                        Size= os.path.getsize(FileName.strip())
                    except:
                        Date=str(datetime.datetime.now())
                        Size=0
                    debugPrint(Date)
                    strQuery="insert into FileNames(path, name, date, size)values('@filename','@filepath','@filedate','@n')"
                    strQuery=strQuery.replace('@filename',FileName)
                    FileName=FileName.split("/")
                    strQuery=strQuery.replace('@filepath',FileName[len(FileName)-1])

                    strQuery=strQuery.replace('@filedate',str(Date))
                    strQuery=strQuery.replace('@n',str(Size))

                    debugPrint(strQuery)
                    cur.execute(strQuery)
                else:
                    debugPrint("FileName not stored: " + FileName)

    except sqlite3.Error as error:
        print("Error Executing query")
        print(str(error.args[0]))
    finally:
        con2.commit()
        con2.close()

def sql_table():
    try:
         cursorObj = FetchCursor()

         strQuery="CREATE TABLE FileNames(id integer PRIMARY KEY AUTOINCREMENT, name text, path text, fullpath text, date text, size text)"
         try:
             cursorObj.execute(strQuery)
             print("Executing:  " + strQuery)
         except:
             print("Error during creation..db already there ?")

         finally:
             strQuery="CREATE TABLE Extentions(id integer PRIMARY KEY AUTOINCREMENT, Ext text, Count text)"
             cursorObj.execute(strQuery)
             print("Executing:  " + strQuery)

             cursorObj.commit()
             print("YOLO!")
    except Error:
        print(Error)
    finally:
        # con.close()
        return cursorObj


def FetchCursor():
    try:
        debugPrint("Entering FetchCursor")
        con =sql_connection()
        cursorObj = con.cursor()
        print("Fetching cursor")
        datetime.SleepSeconds(0.01)
    except Error:
        print("Error fetching cursor")
        print(Error)
    finally:
        return cursorObj

def sql_connection():
    try:
        #con = sqlite3.connect(':memory:')
        #print("Connection is established: Database is created in memory")
        con = sqlite3.connect(vars.strDbName)
        #print("Connection is established: Database is created in file.db")
        debugPrint("sql_connection()")
    except Error:
        print(Error)
    finally:
        # con.close()
        return con

def ShowAllFiles():
    print("Executing Show All Files")
    #con=sql_connection()
    cursorObj=FetchCursor()
    strQuery="Select distinct name, path, date, size from FileNames"
    try:
        cursorObj.execute(strQuery)
    except Error:
        print("Error: " + str(Error))
    rows = cursorObj.fetchall()
    strRet=""
    for row in rows:
        if(len(strRet)>0):
            strRet=strRet + "@" +  str(row[0] + "#" + row[1] + "#" + row[2]+ "#" + row[3])
            #debugPrint(strRet)
        else:
            strRet= str(row[0] + "#" + row[1] + "#" + row[2]+ "#" + row[3])

    return strRet

def executeQuery(strQuery):
    try:
        print("Preparing to execute query")
        cursorObj = FetchCursor()
        print("Cursor Fetched")
        cursorObj.execute(strQuery)
        print("Query executed")
        print("Executing:  " + strQuery)
        print("Commiting..no way back now")
        con.commit()
        print("YOLO!")
    except Error:
        print("Error Executing")
    finally:
        con.close()
        return "Query Executed: " + strQuery


def returnFilePathToStore(strFilePath):
    strFileName = str(strFilePath).replace("[","").replace("'","").replace("]","").replace("//","/").strip()
    debugPrint("FileName convertion from:")
    debugPrint(str(strFilePath))
    debugPrint("to")
    debugPrint(str(strFileName))

    return strFileName



def FileAlreadyStored(strFileName):
    strCount="0"
    try:
        debugPrint("Entering FileAlreadyStored")
        #cursorObj2 = FetchCursor()
        with sqlite3.connect("file.db") as con3:
            cursorObj3 = con3.cursor()
            debugPrint("Cursor fetched")
            strFileName1 = returnFilePathToStore(str(strFileName[0]))
            #strQuery2="select count(*) from FileNames where name='" + str(strFileName1) + "'"
            strQuery="select count(*) from Filenames"
            debugPrint("Query build")
            try:
                debugPrint("Query: " + str(strQuery2))
                #tm.SleepSeconds(0.5)
                try:
                    cursorObj3.execute(strQuery2)
                except Error:
                        print("Error executing cursorobj3")
                        print(str(Error))

                print("Executing:  " + strQuery2)
                strCount = cursorObj3.fetchone()[0]
                print("Count " + str(strCount))
            except sqlite3.Error as error:
                print("Error in FileAlreadyStored")
                print(str(error))
                strCount="0"
            except Error:
                print("Error Executing FileAlreadyStored")
                print(sqlite3.Error)
                strCount="0"
    except Error:
        print("Error Executing FileAlreadyStored")
        print(sqlite3.Error)
        strCount="0"
    finally:
        #debugPrint("Finilizing FileAlreadyStored with " + str(strCount))
        if con3:
            con3.close()
            if strCount=="0":
                return False
            else:
                return True


def showInfo():
    print("showing information")


    cursorObj = FetchCursor()
    #what do we want to see:
        #the db used
        #the number of files StoreFileList
    strQuery="select count(*) from FileNames"
    cursorObj.execute(strQuery)
    print("Executing:  " + strQuery)
    strInfo = cursorObj.fetchone()[0]
    debugPrint(strInfo)

    strQuery="select distinct count(path) from FileNames"
    cursorObj.execute(strQuery)
    print("Executing:  " + strQuery)
    strInfo2 = cursorObj.fetchone()[0]

    strMP3 = showGetInfoOnFileExtention("mp3")
    strWav = showGetInfoOnFileExtention("wav")
    strflv = showGetInfoOnFileExtention("flv")
    strAvi = showGetInfoOnFileExtention("avi")

    return str(strInfo) , str(strInfo2), str(strMP3), str(strWav), str(strflv), str(strAvi)

def GetSummery(strWhere, strDivName):
        cursorObj = FetchCursor()
        #strQuery="select distinct count(path) from FileNames where path like '" + chr(iStartChar) +  "%'"
        strQuery="select distinct count(path) from FileNames where " + str(strWhere)
        cursorObj.execute(strQuery)
        print("Executing:  " + strQuery)
        strDistct = cursorObj.fetchone()[0]
        #strQuery="select count(path) from FileNames where path like '" + chr(iStartChar) +  "%'"
        strQuery="select count(path) from FileNames where " + str(strWhere)

        cursorObj.execute(strQuery)
        print("Executing:  " + strQuery)
        strCount = cursorObj.fetchone()[0]

        print("Gathering all information")
        strHTML=          "<div class='Summery'>\n"
        strHTML=          "<div class='" + strDivName + "'>\n"
        #strHTML=strHTML + "    <div class='" + strDivName +  "'><br>\n"
        #strHTML=strHTML + "         <div class='Header_" + strDivName + "'><br>\n"
        strHTML=strHTML + "         <hr>"
        strHTML=strHTML + "             %REPLACE%"
        strHTML=strHTML + "         <hr>"
        strHTML=strHTML + "         Number of files: %NUM_FILES%<br>\n"
        strHTML=strHTML + "         Unique files:    %NUM_UNIFILES%<br>\n"
        #strHTML=strHTML + "         </div><br>"
        #strHTML=strHTML + "     </div><br>"
        strHTML=strHTML + "</div><br>"

        strHTMLFILE=""

        #strQuery="select path from FileNames where path like '" + chr(iStartChar) +  "%' limit 5"
        strQuery="select path from FileNames where " + strWhere + " limit 5"
        print("Executing:  " + str(strQuery))
        cursorObj.execute(strQuery)

        rows = cursorObj.fetchall()
        for row in rows:
            print(row)
            for cell in row:
                print(cell)
                strHTMLFILE=strHTMLFILE + str(cell) + "<br>\n"

        strHTML=strHTML.replace("%REPLACE%", strHTMLFILE).replace("%NUM_FILES%", str(strDistct)).replace("%NUM_UNIFILES%", str(strCount))
        return strHTML


def showGetInfoOnFileExtention(strFileExtention):
    print("showing Picture information")
    cursorObj = FetchCursor()
    #what do we want to see:
        #the db used
        #the number of files StoreFileList
    strQuery="select distinct count(path) from FileNames where path like '%." + strFileExtention + "'"
    cursorObj.execute(strQuery)
    print("Executing:  " + strQuery)
    return cursorObj.fetchone()[0]

def showPictureInfo():
    print("showing Picture information")
    cursorObj = FetchCursor()

    strBMP = showGetInfoOnFileExtention("bmp")
    strJPG = showGetInfoOnFileExtention("jpg")
    strpng = showGetInfoOnFileExtention("png")
    strTiff = showGetInfoOnFileExtention("tif*")

    return str(strBMP) , str(strJPG), str(strpng), str(strTiff)

def showDocumentInfo():
    print("showing Picture information")
    cursorObj = FetchCursor()

    strDOC = showGetInfoOnFileExtention("doc")
    strDOCX = showGetInfoOnFileExtention("docx")
    strODT = showGetInfoOnFileExtention("odt")
    strTXT = showGetInfoOnFileExtention("txt")

    return str(strDOC) , str(strDOCX), str(strODT), str(strTXT)

def showProjectInfo():
    print("showing Project Programming information")
    cursorObj = FetchCursor()

    strPY = showGetInfoOnFileExtention("py")
    strC = showGetInfoOnFileExtention("suo")
    strBAS = showGetInfoOnFileExtention("bas")
    strH = showGetInfoOnFileExtention("h")
    strCPP = showGetInfoOnFileExtention("cpp")

    strPY_L = GetSummery(" path like '%.py' and path not like '__init__.py'", "projectsummery")
    strC_L = GetSummery(" path like '%.suo'", "projectsummery")
    strBAS_L = GetSummery(" path like '%.bas'", "projectsummery")
    strH_L = GetSummery(" path like '%.h'", "projectsummery")
    strCPP_L = GetSummery(" path like '%.cpp'", "projectsummery")


    return str(strPY) , str(strC), str(strBAS), str(strH), str(strCPP),str(strPY_L) , str(strC_L), str(strBAS_L), str(strH_L), str(strCPP_L)


def getOverAllSummery():
    #lets loop the next 26 chars
    strHTML=""
    for iStartChar in range(65, (62+29)):
        #strHTML= strHTML + GetSummery(iStartChar)
        strWhere = " path like '" + chr(iStartChar) +  "%'"
        strHTML= strHTML + GetSummery(strWhere, "overAllSummery")
    return strHTML

def getALlStoredFileExtentions():
    print("showing Picture information")
    cursorObj = FetchCursor()
    #what do we want to see:
        #the db used
        #the number of files StoreFileList
    list=[]
    strQuery="select distinct path from FileNames"
    cursorObj.execute(strQuery)
    print("Executing:  " + strQuery)
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)
        for cell in row:
            print(cell)
            iLenght=[len(cell)-1]
            print(str(iLenght))
            strExt=mw.getFileExtention(cell[len(cell)-1])
            if not cell in list:
                list.append(str(cell))
    return list

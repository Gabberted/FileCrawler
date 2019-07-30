import FrameWork.debug as debug
from sqlite3 import Error
import os
import app.db as db
import FrameWork.debug as debug

def crawlDir(rootdir):
    debug.debugPrint("Entering crawlDir")
    FileList=[]
    try:
        iFileCounter=0
        for dirs, subdirs, files  in os.walk(rootdir):
            for file in files:

                print("==================  new file ==================  ")
                strFilePath=dirs + "/" +  str(file)
                print(str(strFilePath))

                db.storeSingeFile(str(strFilePath))
                #We need to check if the path is already stored
                #if so we can update the counter
                FileList.append(strFilePath)
                iFileCounter=iFileCounter+1
                print("===============================================  ")

    except Error:
        print(Error)
    finally:
        print("Finally")

    debug.debugPrint("Files found: " + str(iFileCounter))

    return str(FileList)

def Crawl(rootdir):
    strBuilder="Crawling directory " + rootdir
    FileNames=crawlDir(rootdir)

    #now lets save the FileNames found
    #db.StoreFileList(FileNames)

    debug.debugPrint("Exiting Crawl()")
    return FileNames

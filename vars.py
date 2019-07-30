#variables
#rootdir ='/media/rakaut/Seagate/Data/'
#rootdir ='/media/rakaut/Seagate/Data/Desktop/'
#rootdir ='/home/rakaut/Desktop/TestFolder/'
#rootdir ='/home/rakaut/smb:/LGNAS/Private/'
#rootdir ='/media/rakaut/Seagate/Data/Work/Freelans/'
#rootdir ='/mnt/owncloud/'
rootdir ='/mnt/owncloud/MultiMedia/'
strDbName='file.db'

#cursorObj = con.cursor()
print("Fetching cursor")
lstWords=['']
strHTMLHeader="<HTML><TITLE>File Crawler</TITLE><BODY>These are the files in the database: <BR></BODY></HTML>"


#location middleware
_indexFile="html/index.html.cms"
_WelcomeFile="html/Welcome.html.cms"
_infoFile="html/info.html.cms"
_FooterFile="html/footer.html.cms"
_AdminFile="html/Admin.html.cms"
_DoneFile="html/done.html.cms"
_CrawlFile="html/crawl.html.cms"

_StyleSheet="html/style.css"

_btnCrawlFolder="html/CrawlButton.html.css"

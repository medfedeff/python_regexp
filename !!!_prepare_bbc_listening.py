import urllib.request
import os, errno, shutil
from datetime import date
from smart_rename import SmartFileRenamer
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self, KeyWordsList=[]):
        "Parse HTML page for links which have a keyword"
        HTMLParser.__init__(self, True)
        self.__hyperlinks = []
        self.__keyWords = KeyWordsList
        
    def __isValueWithKeyword(self, value):
        for key in self.__keyWords:
            if value.rfind(key) != -1:
                return True
        return False

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if (name == "href") & self.__isValueWithKeyword(value):
                self.__hyperlinks.append(value)

    @staticmethod
    def extractLinksFromUrl(url, keywords):
        url = urllib.request.urlopen(url)
        page = url.read().decode('utf-8')
        parser = MyHTMLParser(keywords)
        parser.feed(page)
        return parser.__hyperlinks

class BbcFilesDownloader:
    def __init__(self, urlsToPdfMp3, folder):
        self.urlsToPdfMp3 = urlsToPdfMp3
        self.urlsToContainers = []
        self.brokenUrls = []
        self.folder = folder

    def __downloadFile(self, url, path, trackBrokenUrls):
        file_name = url.split('/')[-1]
        container_url = url.rpartition('/')[0]        
        try:
            u = urllib.request.urlopen(url)
        except:
            if trackBrokenUrls == True:
                print("\n ******* ERROR: cannot download ", url)
                self.brokenUrls.append(url)
            return False
        else:
            if trackBrokenUrls == True:
                self.urlsToContainers.append(container_url)
            print("\ndownloading: ", url)
            f = open(path + '/' + file_name, 'wb')
            f.write(u.read());
            f.close()
            return True

    def download_with_troubleshooting(self):
        for url in self.urlsToPdfMp3:            
            self.__downloadFile(url, self.folder, True)
        
        for url in self.brokenUrls:
            print('\nTroubleshooting: ', url)
            uri = url.split('/')[-1]
            for contaiter in self.urlsToContainers:
                link = contaiter + '/' + uri
                print('    trying ', link)
                if self.__downloadFile(link, self.folder, False) == True:
                    break
            
        
class Mp3TagGainCorrector:
    def __init__(self, folder, mp3_tag):
        self.folder = folder
        self.mp3_tag = mp3_tag

    @staticmethod
    def __isMp3(s):
        if s.find(".mp3") == -1:
            return False
        else:
            return True

    def exec(self):
        dirList = os.listdir(self.folder)
        dirList = filter(self.__isMp3, dirList)
        for filename in dirList:
            print("correcting MP3 tag & gain in ", filename)
            os.system('id3 -2 -t ' + os.path.splitext(filename)[0] + 
                ' -a ' + self.mp3_tag + 
                ' -l ' + self.mp3_tag +
                ' ' + self.folder + '\\' + filename) 
            os.system('mp3gain /a /c ' + self.folder + '\\' + filename)    

if __name__ == "__main__":

    #get url to BBC download page
    # not available  "http://www.bbc.co.uk/worldservice/learningenglish/" with tag "download.shtml"

    #downloadUrl = MyHTMLParser.extractLinksFromUrl("http://www.bbc.co.uk/learningenglish/", ["downloads"])[0]
    downloadUrl = "http://www.bbc.co.uk/learningenglish/english/course/lower-intermediate/unit-15/downloads"
    print("\ndownloading page:", downloadUrl)

    #get all links to *.pdf and *.mp3
    urlsToPdfMp3 = MyHTMLParser.extractLinksFromUrl(downloadUrl, [".mp3", ".pdf"])
    print("\nMp3&Pdf files found: ", len(urlsToPdfMp3))

    #create folder
    folder = date.today().strftime("bbc_learn_%y_%m_%d")
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

    #downloading all filesfiles
    bbcFilesDownloader = BbcFilesDownloader(urlsToPdfMp3, folder)
    bbcFilesDownloader.download_with_troubleshooting()

    SmartFileRenamer.exec(folder, True)

    #change tags in *.mp3 files
    mp3Corrector = Mp3TagGainCorrector(os.getcwd() + "\\" + folder, folder) #use folder name as mp3_tag
    mp3Corrector.exec()
	
    os.system("pause")
	
	
    
    








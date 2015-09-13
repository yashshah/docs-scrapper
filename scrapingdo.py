from bs4 import BeautifulSoup
import requests
import Queue
from Queue import Queue
q = Queue(maxsize = 50)
base_string = "https://www.digitalocean.com"
def startscrapdocs(sourcelink,storepath):
        print "In startscrapdocs"
        q.put(sourcelink)
        if not q.empty():
                scrapdocs(storepath)
def storefile(storepath,fname,content):
	print "making file "+fname + " in storepath mentioned"
	f = open(storepath+"/"+fname,"ab+")
	f.writelines(content)
	f.close()
	
def scrapdocs(storepath):
        while not q.empty():
                sent_headers = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0",
"domain":"digitalocean.com",
"refer":"http://www.google.com"}
                r = requests.get(q.get(), headers = sent_headers)
                soup = BeautifulSoup(r.content,'lxml')
                fname = soup.find('title').string
                print "processing " + fname
                storefile(storepath,fname,r.content)
                for link in soup.find_all('a'):
                        href = link.get('href')
                        print href
                        if href is not None and "/community/tutorials/" in href:
                                q.put(base_string + href)
                                print href+" put in queue"
                                if q.full():
                                        break
##                if soup.find('code') is not None:
##                        comment = soup.find('code').contents[0]
##                        if comment is not None:
##                                commentsoup = BeautifulSoup(comment)
##                                for link in commentsoup.findAll('a'):
##                                        href = link.get('href')
##                                        if href is not None:
##                                                q.put(base_string + href)
##                                                if q.full():
##                                                        break
                print "done with "+ fname
                if q.full():
                        break        
if __name__ == "__main__":
        startscrapdocs("https://www.digitalocean.com/community/tutorials/",
                               "/home/abhishek/scrapingwork")
        

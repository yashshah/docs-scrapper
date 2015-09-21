from bs4 import BeautifulSoup
import requests
import Queue
from Queue import Queue
from random import randint
from time import sleep
import os
import urlparse
q = Queue()
base_string = "https://www.digitalocean.com"
def startscrapdocs(sourcelink):
        print "In startscrapdocs"
        q.put(sourcelink)
        if not q.empty():
                scrapdocs(os.getcwd())
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
		link_to_call = q.get()
		print ("link to call is "+link_to_call)
		sleep(randint(1,5));
                r = requests.get(link_to_call, headers = sent_headers)
                soup = BeautifulSoup(r.content,'lxml')
                fname = soup.find('title').string
                print "processing " + fname
                storefile(storepath,fname,r.content)
                for link in soup.find_all('a'):
                        href = link.get('href')
                        print href
                        if href is not None and "/community/tutorials/" in href:
				valid_url = urlparse.urljoin(base_string,href)
				if valid_url.startswith(base_string):
                           		q.put(valid_url)
                                	print valid_url
##                               if q.full():
##                                       break
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
        startscrapdocs("https://www.digitalocean.com/community/tutorials/")
        

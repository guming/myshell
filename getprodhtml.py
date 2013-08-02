import sys,string
import Queue,threading
import time,urllib2,os,json
basedir = '/opt/source/test/product/'
purl_prefix = 'http://10.1.200.80/product/'
class WorkManager(object):
  def __init__(self,threadNum=16,pstr=file('pids.txt')):
		self.workQueue=Queue.Queue()
		self.threads=[]
		self.initWorkQueue(pstr)
		self.initThread_pool(threadNum) 
	def initWorkQueue(self,pstr):
		while True:
			pid = pstr.readline()
			if len(pid) == 0:
				break
                        if string.atoi(pid)<=105282:
				continue
			pid = pid.strip()
			url=purl_prefix+pid+".html"
			if pid!='':
				self.addJob(do_job,pid,url)
		pstr.close()
			
	def initThread_pool(self,threadNum):
		for i in range(threadNum):  
			self.threads.append(Work(self.workQueue))
	def addJob(self, func, *args):
		self.workQueue.put((func, list(args)))
	def wait_allcomplete(self):
		for item in self.threads:  
			if item.isAlive():
				item.join()

class Work(threading.Thread):  
    def __init__(self, workQueue):  
        threading.Thread.__init__(self)  
        self.workQueue = workQueue  
        self.start()    
    def run(self):
		while True:
			try:
				do,args = self.workQueue.get(block=False)
				do(args)
				self.workQueue.task_done()
			except:
				break
def do_job(args):
    pid=args[0]
    url=args[1]
    print 'pid:',pid
    filename=basedir+pid+".html"
    try:
		response = urllib2.urlopen(url, timeout=10)
		if response.getcode()==200 or response.getcode()==301 or response.getcode()==302 :
			f_dist = file(filename, 'w')
			f_dist.write(response.read())
                        f_dist.close()
    except urllib2.HTTPError,e:
        print url, e.code
        print e.reason
    except urllib2.URLError,e:
        print e.reason
    else:
		pass
		
def getprodhtml():
	f_source = file('pids.txt')
	start_time = time.time()
	work_manager=WorkManager(4,f_source)  
	work_manager.wait_allcomplete()  
	time_span = time.time() - start_time
	print "executed time:",  time_span
getprodhtml()


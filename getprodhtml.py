import gevent
import time,urllib2,os,json
from gevent.pool import Pool
basedir = '/opt/source/test/product/'
purl_prefix = 'http://10.1.200.80/product/'
pool=Pool(4)
def do_job(pid):
    url=purl_prefix+pid+".html"
    filename=basedir+pid+".html"
    print 'pid:',pid
    try:
                response = urllib2.urlopen(url, timeout=60)
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
        with file('pids.txt') as f_source:
            while True:
                        pid = f_source.readline()
                        if len(pid) == 0:
                                break
                        pid = pid.strip()
                        if pid!='':
                                pool.spawn(do_job,pid)
getprodhtml()


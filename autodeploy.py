#!/usr/bin/env python
#coding=utf-8
from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
from fabric.colors import red, green
from fabric.contrib.files import append

import datetime
import time
env.hosts = ['10.1.200.80','10.1.200.82']
env.exclude_hosts=['10.1.200.80']
env.password='xxxxxxx'
env.command_timeout=180
env.timeout=3
env.connection_attempts=3


resin_home='/opt/priceimg/'
resin_shell='sh resin_price.sh'
checklive_url="curl 'http://127.0.0.1:8091/generateImage/image/isLive.html'"

def freeM():
    output=run('free -m')
    print output

def nginxRestart():
    output=sudo("/opt/nginx-1.2.7/sbin/nginx -c /opt/nginx-1.2.7/conf/nginx.conf -s reload")
    print output

def resinRestart():
    running=True
    with cd(resin_home):
    	output=run(resin_shell)
    	print output
    time.sleep(10)
    while running:
	result=checkstat()	
        if result==True:
             running=False
             break
        else:
             time.sleep(10)

def nginxStop():
     output=run("/opt/nginx-1.2.7/sbin/nginx -s stop")
     print output

def nginxStart():
     output=run("/opt/nginx-1.2.7/sbin/nginx -c /opt/nginx-1.2.7/conf/nginx.conf")
     print output

def checkstat():
    output=run(checklive_url)
    print("Executing on %s as %s" % (env.host, env.user))
    if output.strip()=='live!':
       print 'the resin has been started'
       return True
    else:
       print 'the resin failed to start'
       return false

def codeupdate():
     with cd('/opt/priceimg'):
     	output=run('sh antshell.sh')
        print("Executing on %s as %s" % (env.host, env.user))
        if output.find('BUILD SUCCESSFUL')!=-1:
                print 'antshell run successed!'
		return True
        else:
		return False

def deploy():
     result=confirm("Dou you want to do this?")
     if result==True:
     	#!/usr/bin/env python
#coding=utf-8
from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
from fabric.colors import red, green
from fabric.contrib.files import append

import datetime
import time
env.hosts = ['10.1.200.80','10.1.200.82']
env.exclude_hosts=['10.1.200.80']
env.password='xxxxxxx'
env.command_timeout=180
env.timeout=3
env.connection_attempts=3


resin_home='/opt/priceimg/'
resin_shell='sh resin_price.sh'
checklive_url="curl 'http://127.0.0.1:8091/generateImage/image/isLive.html'"

def freeM():
    output=run('free -m')
    print output

def nginxRestart():
    output=sudo("/opt/nginx-1.2.7/sbin/nginx -c /opt/nginx-1.2.7/conf/nginx.conf -s reload")
    print output

def resinRestart():
    running=True
    with cd(resin_home):
    	output=run(resin_shell)
    	print output
    time.sleep(10)
    while running:
	result=checkstate()	
        if result==True:
             running=False
             break
        else:
             time.sleep(10)

def nginxStop():
     output=run("/opt/nginx-1.2.7/sbin/nginx -s stop")
     print output

def nginxStart():
     output=run("/opt/nginx-1.2.7/sbin/nginx -c /opt/nginx-1.2.7/conf/nginx.conf")
     print output

def checkstate():
    output=run(checklive_url)
    print("Executing on %s as %s" % (env.host, env.user))
    if output.strip()=='live!':
       print 'the resin has been started'
       return True
    else:
       print 'the resin failed to start'
       return false

def codeupdate():
     with cd('/opt/priceimg'):
     	output=run('sh antshell.sh')
        print("Executing on %s as %s" % (env.host, env.user))
        if output.find('BUILD SUCCESSFUL')!=-1:
                print 'antshell run successed!'
		return True
        else:
		return False

def deployserial():
     result=confirm("Dou you want to do this?")
     if result==True:
     	codeupdate()
     	resinRestart()

@parallel(4)
def deployall():
     print(green("This parallel tasks are starting!"))
     with hide('running','stdout'):
     	codeupdate()
     	resinRestart()


@hosts('10.1.200.80')
def deploysingle():
     confirm("Dou you want to do this?")
     result=codeupdate()
     if result == True:
     	resinRestart()

     	


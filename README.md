myshell
=======

the shells
-------------
*    1.javakiller.sh  kill java process and export the jstack dump to the file
*    2. getprodhtml.py  使用gevent,抓取知道商品的url,并保存至磁盘
*    3. quciklz.lua   quicklz的lua代码，参考自：http://luajit.org/ext_ffi_tutorial.html  
     解决通过openresty试用memcached的压缩和解压缩问题  
     其中quicklz15.so  是编译后的so文件，lua里有引用  
     自行编译：  
      http://www.quicklz.com/download.html 下载c语言的quicklz.c quicklz.h  
      生成so文件:  
      gcc quicklz.c -shared -fPIC -o quicklz1.5.so  
      生成lua的type:  
      gcc -P -E quicklz.h


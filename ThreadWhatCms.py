#!/usr/bin/python 
#coding:utf-8 
import threading 
import datetime 
import logging 
import time
import random
import os,sys
import urllib2
import hashlib
import re
import getopt
from libs.WhatcmsColor import *

# 设置调试信息
logging.basicConfig(level = logging.DEBUG,format='(%(threadName)-10s) %(message)s',) 
#需要匹配的文件列表，即表示需要和这些文件进行匹配对比
file_list = []
# 程序运行的路径
root_path                 =  ""
# md5 文件所在路径
md5_file_path             =  os.sep + "md5" + os.sep
# robots 文件所在路径
robots_file_path          =  os.sep + "robots" + os.sep
# 学习模式目录匹配文件所在路径
directory_file_path       =  os.sep + "directory" + os.sep
# 已经学习的目录路径
dir_has_matched_file_path =  os.sep + "dir_has_matched_file_path" + os.sep
# 浏览器标识
UserAgent                 =  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.0.0 Safari/537.36'
#######################需要处理的 host #############################
host_url = ''


class Test(threading.Thread): 
    def __init__(self,threadingSum, file_name): 
        threading.Thread.__init__(self) 
        self.file_name = file_name 
        self.threadingSum = threadingSum 
                                                              
    def run(self): 
        with self.threadingSum: 
            logging.debug("%s start ......" % self.file_name)
            fp = open(root_path + dir_has_matched_file_path + self.file_name,"r")
            lines = fp.readlines() # 需要处理的urls
            fp.close()
            for line in lines:
                if len(line)==0:
                    continue
                if line == "\n":
                    continue
                if line == "\r\n":
                    continue
                if self.get_url_code(host_url+line):
                    color.cprint("[*] [dir]=> " + self.file_name[:-4] + " => " + host_url + line,CYAN)
                else:
                    color.cprint("[*] [dir]=> " + self.file_name[:-4] + " => " + host_url + line,YELLOW)
            time.sleep(random.randint(1,3)) 
            logging.debug('%s Done ......' % self.file_name) 
            
    def get_url_code(self,url):
        req = urllib2.Request(url)
        req.add_header('User-Agent',UserAgent)
        req.add_header('Referer','http://www.baidu.com')
        try:
            res = urllib2.urlopen(req,timeout=5)
            if res.getcode() == 200:
                return True
            else:
                return False
        except Exception,e:
            #print e
            return False
                                                                  

                                                              
if __name__ == "__main__":
    # 获得当前程序所在的目录
    root_path = os.getcwd()
    #################################关键代码，需要完成的任务，这里为需要处理的文件######################################
    file_list = os.listdir(root_path + dir_has_matched_file_path)
    #################################关键代码，需要完成的任务，这里为需要处理的文件######################################
    #设置线程数 
    threadingSum = threading.Semaphore(4) 
    
    
    ################################# 关键代码  要扫描的主机        ####################################
    host_url = 'http://www.freebuf.com'
    
    ## 启动线程
    for file_name in file_list:
        f = Test(threadingSum,file_name)
        f.start()
        
    ## 等待所有线程结束
    for w in threading.enumerate():
        if w is threading.currentThread():
            continue
        w.join()
                                                              
    logging.debug('Done .....')
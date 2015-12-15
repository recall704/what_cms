#encoding=utf-8

import threading
import os
import sys
import urllib2
import time
from random import randint
from libs.WhatcmsColor import *


def get_file_list():
    file_list = os.listdir(os.getcwd()+os.sep+"dir_has_matched_file_path")
    return file_list

def get_url_status_code(url):
    req = urllib2.Request(url)
    try:
        res = urllib2.urlopen(req,timeout=5)
        if res.getcode()==200:
            return True
        else:
            return False
    except:
        return False



class Tester(threading.Thread):
    def __init__(self,name,file_path):
        threading.Thread.__init__(self)
        self.name = name
        self.path = file_path
        self.thread_stop = False
    def run(self):
        if not self.thread_stop:
            host = "http://www.freebuf.com"
            print "handle %s => %s,time = %s\n" %(self.name,self.path,time.ctime())
            f = open(os.getcwd()+os.sep+"dir_has_matched_file_path"+os.sep+self.name)
            lines = f.readlines()
            f.close()
            match_count = 0
            for ll in lines:
                time.sleep(1)
                if get_url_status_code(host+ll):
                    color.cprint(self.name+ll,GREEN)
                    match_count +=1
                else:
                    color.cprint(ll,YELLOW)
                if match_count > 20:
                    sys.exit()
                
    def stop(self):
        self.thread_stop = True



if __name__ == "__main__":
    file_list = get_file_list()
    for fileItem in file_list:
        p = Tester(fileItem,"/test/")
        p.start()
        

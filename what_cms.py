#!/usr/bin/env python
#coding:utf-8


from libs.WhatcmsColor import *
import os,sys
import urllib2
import hashlib
import re
import getopt





UseageInfo = """
        Usage:
            -h --help           帮助信息
            -m --md5            使用md5匹配算法，加上-m表示使用，不加表示不使用
            -d --directory      使用目录对比算法，加上表示使用，不加表示不使用
            -r --robots         使用robots对比算法，使用方法同上
            -u --url            要查询的URL
            -l --learn          学习模式，建议只是用一次
        说明:
	    参数-u 是必须的，如果网站存在目录，请加上目录，比如www.***.com/phpcms
	    最好一次选择一个匹配算法，同时使用会有过多的显示信息
            默认使用md5匹配算法
"""



root_path           = ""
md5_file_path       = os.sep + "md5" + os.sep
robots_file_path    = os.sep + "robots" + os.sep
directory_file_path = os.sep + "directory" + os.sep
dir_has_matched_file_path = os.sep + "dir_has_matched_file_path" + os.sep
UserAgent           = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.0.0 Safari/537.36'


#定义帮助信息
def usage():
    print(os.linesep)
    print("*"*100)
    print(os.linesep)
    color.cprint(u"\twhat_cms是一个web应用程序指纹识别工具,可自动识别CMS、BLOG等Web系统，主要针对国内的discuz、",YELLOW)
    color.cprint(u"\tdede、帝国、PHPCMS等",YELLOW)
    print(os.linesep)
    color.cprint(UseageInfo.decode("UTF-8"),GREEN)
    print(os.linesep)
    print("*"*100)
    sys.exit()


#定义md5 匹配方法
def md5_match_method(host):
    
    def get_md5_file_list():
        return os.listdir(root_path + md5_file_path)
    
    def get_html(url):
        url = url.strip()
        html = urllib2.urlopen(url).read()
        return html
    def get_md5(html):
        m = hashlib.md5()
        m.update(html)
        md5 = m.hexdigest()
        return md5
    
    #获得文件列表
    file_list = get_md5_file_list()
    #遍历所有文件
    for fileItem in file_list:
        f = open(root_path + md5_file_path + fileItem,"r")
        lines = f.readlines()
        f.close()
        for line in lines:
            list_ll = line.split("::")
            _url = list_ll[0]  #资源路径
            _md5 = list_ll[1]  #匹配md5
            _cms = list_ll[2]  #cms 名称
            try:
                color.cprint("[*] [md5]=> [" + fileItem + "] ======> " + host + _url,YELLOW)
                _html = get_html(host + _url)
                page_md5 = get_md5(_html)
                if page_md5 == _md5:
                    result = host + " => " + _cms
                    color.cprint("[!] [md5]=> [Congratulations!] => " + result,GREEN)
                    return
            except Exception,e:
                #color.cprint('[!] Error=>'+str(e),RED)
                pass
    return "Matched Falied By md5 method"

#定义robots方法
def robots_match_method(host):
    #print host
    def get_robots_file_list():
        return os.listdir(root_path + robots_file_path)
    def get_robots_web_lines(host):
        url = host + "/robots.txt"
        request = urllib2.Request(url)
        request.add_header('User-Agent',UserAgent)
        request.add_header('Referer','http://www.baidu.com')
        try:
            response = urllib2.urlopen(request)
            if response.getcode()==200:
                return response.readlines()
        except Exception,e:
            color.cprint('[!] Error=> '+str(e),RED)
            return []
                
        
    file_list    = get_robots_file_list()
    robots_lines = get_robots_web_lines(host)
    result_dict = {} #匹配完整结果集
    if len(robots_lines)==0:
        color.cprint("[*] [robots]=> robots.txt file not found!",RED)
        return
    
    #匹配Power By
    for line in robots_lines:
        m = re.search(r"robots.*for.*",line,re.I)
        if m:
            color.cprint("[!] [robots]=> [Congratulations!] => " + line[line.find("for")+3:],GREEN)
        n = re.search(r"power.*by.*",line,re.I)
        if n:
            color.cprint("[!] [robots]=> [Congratulations!] => " + line[line.find("by")+2:],GREEN)
    #遍历所有文件
    for fileItem in file_list:
        f        = open(root_path + robots_file_path + fileItem,"r")
        txtLines = f.readlines()
        txtLines = list(set(txtLines))#去掉重复项
        f.close()
        match_count = 0 #匹配数量
        cms_name    ='' #匹配cms名称
        for line in txtLines:
            mm = re.search(r"Disallow",line) #进匹配Disallow项
            if mm:
                #color.cprint("[*] [robots]=> " + line,YELLOW)
                if line.rstrip("\r\n")+"\n" in robots_lines:
                    match_count += 1
                elif line.rstrip("\n")+"\r\n" in robots_lines:
                    match_count += 1
        result_dict[fileItem] = match_count
    #处理结果集
    if max(result_dict.values())==0:#所有选项未匹配
        color.cprint("[*] [robots]=> No matched !",RED)
    else:
        result = sorted(result_dict.items(),key =lambda d: d[1],reverse=True)#排序
        color.cprint("[!] [robots]=> [Congratulations!] => " + result[0][0][:-4],GREEN)

#定义目录对比方法，学习模式
def dir_match_method(host):
    #color.cprint(("\t该方法尚未实现，尽请期待！").decode("UTF-8"),RED)
    def get_dir_file_list():
        return os.listdir(root_path + directory_file_path)
    def get_url_code(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent',UserAgent)
        req.add_header('Referer','http://www.baidu.com')
        try:
            res = urllib2.urlopen(req,timeout=5)
            if res.getcode() == 200:
                return True
            else:
                return False
        except:
            return False
    file_list = get_dir_file_list()
    match_count = 0
    result_dict = {}
    for fileItem in file_list:
        f = open(root_path + directory_file_path + fileItem,"r")
        f_new    = open(root_path + dir_has_matched_file_path + fileItem,"w") #保存已匹配的选项到新文件
        lines = f.readlines()
        f.close()
        i = 0
        for line in lines:
            i += 1
            if line == "":
                break
            if get_url_code(host+line):
                color.cprint("[*] [dir]=> " + fileItem[:-4] + " => " + host + line,CYAN)
                match_count += 1
                f_new.writelines(line)         #保存当前匹配项
                #f_new.write(os.linesep)
            else:
                color.cprint("[*] [dir]=> " + fileItem[:-4] + " => " + host + line,YELLOW)
            #if match_count >=10:
                #break
            #if (i>20 and match_count==0):
                #break
        f_new.close()
        result_dict[fileItem] = match_count
    #处理结果集
    if max(result_dict.values())==0:#所有选项都不匹配
        color.cprint("[*] [dir]=> No matched !",RED)
    else:
        result = sorted(result_dict.items(),key = lambda d: d[1],reverse=True)#排序
        for k,v in result:
            if v != 0:
                color.cprint("[*] [dir]=> [Congratulations!] =>" + k[:-4] + " Matched " + str(v) + " Items",GREEN)

#目录匹配模式，已匹配选项
def dir_has_matched_method(host):
    #color.cprint(("\t该方法尚未实现，尽请期待！").decode("UTF-8"),RED)
    def get_dir_file_list():
        return os.listdir(root_path + dir_has_matched_file_path)
    def get_url_code(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent',UserAgent)
        req.add_header('Referer','http://www.baidu.com')
        try:
            res = urllib2.urlopen(req,timeout=5)
            if res.getcode() == 200:
                return True
        except:
            return False
    file_list = get_dir_file_list()
    result_dict = {}
    for fileItem in file_list:
        f = open(root_path + dir_has_matched_file_path + fileItem,"r")
        lines = f.readlines()
        f.close()
        i = 0
        match_count = 0
        for line in lines:
            i += 1
            if len(line)==0:
                continue
            if line == "\n":
                continue
            if line == "\r\n":
                continue
            if get_url_code(host+line):
                color.cprint("[*] [dir]=> " + fileItem[:-4] + " => " + host + line,CYAN)
                match_count += 1
            else:
                color.cprint("[*] [dir]=> " + fileItem[:-4] + " => " + host + line,YELLOW)
            if match_count >=15:
                #color.cprint("[*] [dir]=> It matched 15 Items",GREEN)
                break
            if (i>20 and match_count<5):#如果匹配了20个，匹配数量小于5，就跳出
                break
        result_dict[fileItem] = match_count
    #处理结果集
    if max(result_dict.values())==0:#所有选项都不匹配
        color.cprint("[*] [dir]=> No matched !",RED)
    else:
        result = sorted(result_dict.items(),key = lambda d: d[1],reverse=True)#排序
        for k,v in result:
            if v != 0:
                color.cprint("[*] [dir]=> [Congratulations!] =>" + k[:-4] + " Matched " + str(v) + " Items",GREEN)

#解析url
def url_parse(host,ssl):
    if ssl:
        if host.find("https://")== -1:
            host = "https://" + host
    else:
        if host.find("http://") == -1:
            host = "http://" + host
    return host.rstrip("/")


def main(host,useMd5,useRobots,useDirectory,useSsl,useLearn):
    url = url_parse(host,useSsl)
    try:
        if useMd5:
            md5_match_method(url)
        if useRobots:
            robots_match_method(url)
        if useDirectory:
            dir_has_matched_method(url)
        elif useLearn:
            dir_match_method(url)
        if not (useMd5 or useDirectory or useRobots or useLearn):
            md5_match_method(url)
    except KeyboardInterrupt:
        pass

        
    
if __name__ == "__main__":
    root_path = os.getcwd()
    if len(sys.argv) <2:
        usage()
    try:
        options,args = getopt.getopt(sys.argv[1:],"hmdrslu:",["help","--md5","--directory","--robots","--ssl","--learn","--url"])
    except getopt.GetoptError:
        usage()
    
    host = "http://www.baidu.com"
    useMd5 = False
    useRobots = False
    useDirectory = False
    useSsl = False
    useLearn = False
    
    for name,value in options:
        if name in ("-h","--help"):
            usage()
        if name in ("-m","--md5"):
            useMd5 = True
        if name in ("-d","--directory"):
            useDirectory = True
        if name in ("-r","--robots"):
            useRobots = True
        if name in ("-u","--url"):
            host = value
        if name in ("-s","--ssl"):
            useSsl = True
        if name in ("-l","--learn"):
            useLearn = True
            
    main(host,useMd5,useRobots,useDirectory,useSsl,useLearn)
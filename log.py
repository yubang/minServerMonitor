#coding:UTF-8

"""
日记模块
"""

import time,os

def write(message):
    "记录日记"
    today=time.strftime("%Y%m%d")
    path=os.path.dirname(os.path.realpath(__file__))+"/log/"+today
    fp=open(path,"a")
    fp.write(message.encode("UTF-8"))
    fp.write("\n")
    fp.close()
    

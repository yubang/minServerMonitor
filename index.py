#coding:UTF-8

import os,time,re
from  pyinotify import  WatchManager, Notifier, \
ProcessEvent,IN_DELETE, IN_CREATE,IN_MODIFY

#引入日记处理
import log

#引入邮件处理
import mail

#加入监控模块和忽略正则表达式
watchPath=None
ignoreList=[]

def load():
    global watchPath,ignoreList
    path=os.path.dirname(os.path.realpath(__file__))
    fp=open(path+"/conf/fsPath.conf","r")
    for line in fp:
        line=line.strip()
        if not os.path.exists(line):
            continue
        watchPath=line
    fp.close()
    
    fp=open(path+"/conf/fsIgnore.conf","r")
    for line in fp:
        line=line.strip()
        ignoreList.append(line)
    fp.close()
    
    
def dealMessage(eventType,event):
    global ignoreList
    path=os.path.join(event.path,event.name)
    for r in ignoreList:
        if(re.search(r,path)):
            return None
    message=u"时间：%s 事件：%s 路径：%s"%(time.strftime("%Y%m%d %H:%M:%S"),eventType,path.decode("UTF-8"))
    log.write(message)
    mail.send(message) 
 
class EventHandler(ProcessEvent):
    """事件处理"""
    def process_IN_CREATE(self, event):
        dealMessage("create",event)
 
    def process_IN_DELETE(self, event):
        dealMessage("delete",event)

    def process_IN_MODIFY(self, event):
        dealMessage("update",event)
     
def FSMonitor(path='.'):
    wm = WatchManager() 
    mask = IN_DELETE | IN_CREATE |IN_MODIFY
    notifier = Notifier(wm, EventHandler())
    wm.add_watch(path, mask,auto_add=True,rec=True)
    print 'now starting monitor %s'%(path)
    while True:
        try:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
        except KeyboardInterrupt:
            notifier.stop()
            break
 
 
if __name__ == "__main__":
    load()
    FSMonitor(watchPath)

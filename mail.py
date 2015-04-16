#coding:UTF-8

import smtplib
from email.mime.text import MIMEText

def send(message):
    _user = "hmtclientmonitor@gmail.com"
    _pwd  = ""
    _to   = "hmt_server_monitor@163.com"

    #使用MIMEText构造符合smtp协议的header及body
    msg = MIMEText(message.encode("UTF-8"),_charset='UTF-8')
    msg["Subject"] = u"服务器警告邮件"
    msg["From"]    = _user
    msg["To"]      = _to

    s = smtplib.SMTP("smtp.gmail.com", timeout=30)#连接smtp邮件服务器,端口默认是25
    s.ehlo()
    s.starttls()
    s.login(_user, _pwd)#登陆服务器
    s.sendmail(_user, _to, msg.as_string())#发送邮件
    s.close()


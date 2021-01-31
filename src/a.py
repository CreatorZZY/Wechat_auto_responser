'''
Author: George Zhao
Date: 2021-01-30 17:14:18
LastEditors: George Zhao
LastEditTime: 2021-01-31 13:00:38
Description: 
Email: 2018221138@email.szu.edu.cn
Company: SZU
Version: 1.0
'''
# 源代码如下：
# wechat autoreply
import itchat
import re
import time
import datetime
import pytz


R_SWITCH = False

# 自动回复
# 封装好的装饰器，当接收到的消息是Text，即文字消息
@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing', 'Picture'])
def text_reply(msg):
    # 当消息不是由自己发出的时候
    global R_SWITCH
    if not msg['FromUserName'] == Name["GeorgiZhao"]:
        # 回复给好友
        if R_SWITCH == True:
            return "[自动回复]Hi，抱歉噢，我不在线，有事直接打我手机，或者直接给我留言吧~[LetMeSee]\n{}, HK\nFrom Google Cloud".format(datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Hong_Kong')).strftime('%Y-%m-%d %H:%M:%S'))
    else:
        if msg['Type'] == itchat.content.TEXT:
            if msg['Text'] == 'ON!':
                R_SWITCH = True
                return 'Commanded. R_SWITCH={}'.format('True' if R_SWITCH else 'False')
            elif msg['Text'] == 'OFF!':
                R_SWITCH = False
                return 'Commanded. R_SWITCH={}'.format('True' if R_SWITCH else 'False')
            else:
                pass
        else:
            pass


if __name__ == '__main__':
    itchat.login(enableCmdQR=2)

    # 获取自己的UserName
    friends = itchat.get_friends(update=True)[0:]
    Name = {}
    Nic = []
    User = []
    for i in range(len(friends)):
        Nic.append(friends[i]["NickName"])
        User.append(friends[i]["UserName"])
    for i in range(len(friends)):
        Name[Nic[i]] = User[i]
    itchat.run()

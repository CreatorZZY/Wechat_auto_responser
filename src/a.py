'''
Author: George Zhao
Date: 2021-01-30 17:14:18
LastEditors: George Zhao
LastEditTime: 2021-02-22 17:16:58
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
AutoReply_text_origin = 'Hi，抱歉噢，我不在线，有事直接打我手机，或者直接给我留言吧~[LetMeSee]'
AutoReply_text = AutoReply_text_origin
VERSION = 'gAutoReply v1.0.0'
DEBUG_SWITCH = False

MyUserName = ''

Time_s_To_Wait = 30
dict_that_responsed = dict()

# 自动回复
# 封装好的装饰器，当接收到的消息是Text，即文字消息
@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing', 'Picture'])
def text_reply(msg):
    # 当消息不是由自己发出的时候
    global R_SWITCH
    global AutoReply_text
    global VERSION
    global DEBUG_SWITCH
    global dict_that_responsed
    global Time_s_To_Wait
    if not msg['FromUserName'] == MyUserName:
        # 回复给好友
        if R_SWITCH != True:
            pass
        else:
            if msg['FromUserName'] not in dict_that_responsed or time.time() - dict_that_responsed[msg['FromUserName']] > Time_s_To_Wait:
                dict_that_responsed[msg['FromUserName']] = time.time()
                return "[自动回复]{}\n{}, CN\nFrom Google Cloud".format(AutoReply_text, datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Hong_Kong')).strftime('%Y-%m-%d %H:%M:%S'))
            else:
                pass
    else:
        if msg['ToUserName'] != MyUserName:
            dict_that_responsed[msg['ToUserName']] = time.time()
        if msg['Type'] == itchat.content.TEXT:
            msg_Text = str(msg['Text'])
            if msg_Text[0] == '！':
                msg_Text = msg_Text.replace('！', '!', 1)
            if msg_Text[0] == '!':
                if DEBUG_SWITCH == True:
                    print('* {}'.format(msg_Text))
                msg_Text = msg_Text.upper()
                if msg_Text == '!ON':
                    R_SWITCH = True
                    return 'Commanded. R_SWITCH={}'.format('True' if R_SWITCH else 'False')
                elif msg_Text == '!OFF':
                    R_SWITCH = False
                    return 'Commanded. R_SWITCH={}'.format('True' if R_SWITCH else 'False')
                elif msg_Text.find('!TIMETOWAIT') == 0:
                    l = msg['Text'].split('=', maxsplit=1)
                    try:
                        if len(l) > 1:
                            Time_s_To_Wait = int(l[1])
                            return f'Commanded. TIMETOWAIT={Time_s_To_Wait} seconds.'
                        else:
                            return f'Commanded. TIMETOWAIT Unchange: {Time_s_To_Wait} seconds.'
                    except ValueError as e:
                        return repr(e)
                elif msg_Text == '!VERSION':
                    return VERSION
                elif msg_Text == '!STATUS':
                    return 'STATUS\n* VERSION={VERSION}\n* DEBUG_SWITCH={DEBUG_SWITCH}\n* R_SWITCH={R_SWITCH}\n* AutoReply_text={AutoReply_text}\n* Time={Time}, CN'.format(
                        VERSION=VERSION,
                        R_SWITCH='True' if R_SWITCH else 'False',
                        AutoReply_text=AutoReply_text,
                        DEBUG_SWITCH='True' if DEBUG_SWITCH else 'False',
                        Time=datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone(
                            'Asia/Hong_Kong')).strftime('%Y-%m-%d %H:%M:%S')
                    )
                elif msg_Text == '!DICT':
                    print(msg)
                elif msg_Text == '!DEBUG':
                    if DEBUG_SWITCH == False:
                        DEBUG_SWITCH = True
                    else:
                        DEBUG_SWITCH = False
                    return 'Commanded. DEBUG_SWITCH={}'.format('True' if DEBUG_SWITCH else 'False')
                elif msg_Text.find('!AUTOREPLYTEXT') == 0:
                    l = msg['Text'].split('=', maxsplit=1)
                    if len(l) > 1:
                        AutoReply_text = l[1]
                        return 'Commanded. AutoReply_text Changed: {}'.format(AutoReply_text)
                    else:
                        return 'Commanded. AutoReply_text Unchange: {}'.format(AutoReply_text)
                else:
                    pass
            else:
                pass
        else:
            pass


if __name__ == '__main__':
    itchat.login(enableCmdQR=2)

    # 获取自己的UserName
    friends = itchat.get_friends(update=True)[0:]
    MyUserName = itchat.search_friends()['UserName']
    itchat.run()

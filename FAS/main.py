import telebot
from telebot import types
import dbworker
from config import token
import config
from pathlib import Path
import os
import subprocess
import shutil
import sqlite3
import glob

bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def startmenu(message):
    chat_id = message.chat.id
    cookieexists = len(os.listdir('cookie2'))
    with open ('proxy.txt', 'r') as file:
        q = len(file.readlines())
    with open ('chanels', 'r') as file:
        ge = len(file.readlines())
    bot.send_message(chat_id, '''
             Ready?
            Uploaded proxy:  ''' + str(q) + ''' pieces
            Uploaded channels:  ''' + str(ge) + ''' pieces
            Uploaded cookies: ''' + str(cookieexists) + ''' pieces
            ''', reply_markup=keyboard())
    dbworker.set_state(message.chat.id, config.States.S_START.value)
        
@bot.callback_query_handler(func=lambda message: True)
def menu(message):
    chat_id = message.message.chat.id
    if message.data == 'proxy':
        with open ('proxy.txt', 'r') as file:
                q = len(file.readlines())
        bot.send_message(chat_id, 'Uploaded proxy: ' + str(q) + ' pieces', reply_markup=keyboard4())
        dbworker.set_state(message.message.chat.id, config.States.S_ENTER_PROXY.value)
    if message.data == 'channels':
        with open ('chanels', 'r') as file:
                ge = len(file.readlines())
        bot.send_message(chat_id, 'Uploaded channesl: ' + str(ge) + ' ', reply_markup=keyboard6())
        dbworker.set_state(message.message.chat.id, config.States.S_ENTER_CHANEL.value)
    if message.data == 'FP':
        cookieexists = len(os.listdir('cookie2'))
        bot.send_message(chat_id, 'Uploaded cookie: ' + str(cookieexists) + ' Choose:', reply_markup=keyboard5())
        dbworker.set_state(message.message.chat.id, config.States.S_ENTER_COOKIE.value)
    if message.data == 'back':
        startmenu(message.message)
        dbworker.set_state(message.message.chat.id, config.States.S_START.value)
    if message.data == 'sett':
        bot.send_message(chat_id, 'Set up your bot here', reply_markup=keyboard3())
    if message.data == '1':  
        con = sqlite3.connect('BotDB.db', timeout=2)
        cur = con.cursor()
        cur.execute("SELECT percent FROM settings WHERE log=0")
        per1 = str(cur.fetchone())
        con.commit()
        cur.close()
        con.close()
        per = per1[1:-2]
        con = sqlite3.connect('BotDB.db', timeout=2)
        cur = con.cursor()
        cur.execute("SELECT percentv FROM settings WHERE log=0")
        perv1 = str(cur.fetchone())
        con.commit()
        cur.close()
        con.close()
        perv = perv1[1:-2]
        con = sqlite3.connect('BotDB.db', timeout=2)
        cur = con.cursor()
        cur.execute("SELECT lengh FROM settings WHERE log=0")
        len1 = str(cur.fetchone())
        con.commit()
        cur.close()
        con.close()
        len = len1[1:-2]
        bot.send_message(chat_id, '''
        percent video on channel(%):  ''' + str(per) + '''
        percent clicks on video (%):  ''' + str(perv) + '''
        lengh video (sec):  ''' + str(len) + '''

        ''', reply_markup=keyboard8())

    if message.data == '2':
        con = sqlite3.connect('BotDB.db', timeout=2)
        cur = con.cursor()
        cur.execute("SELECT percent FROM settings WHERE log=0")
        per1 = str(cur.fetchone())
        con.commit()
        cur.close()
        con.close()
        per = per1[1:-2]
        con = sqlite3.connect('BotDB.db', timeout=2)
        cur = con.cursor()
        cur.execute("SELECT percentv FROM settings WHERE log=0")
        perv1 = str(cur.fetchone())
        con.commit()
        cur.close()
        con.close()
        perv = perv1[1:-2]
        con = sqlite3.connect('BotDB.db', timeout=2)
        cur = con.cursor()
        cur.execute("SELECT lengh FROM settings WHERE log=0")
        len1 = str(cur.fetchone())
        con.commit()
        cur.close()
        con.close()
        len = len1[1:-2]
        bot.send_message(chat_id, '''
        percent video on channel(%):  ''' + str(per) + '''
        percent clicks on video (%):  ''' + str(perv) + '''
        lengh video (sec):  ''' + str(len) + '''

        ''', reply_markup=keyboard8())
    if message.data == 'ok':
        startmenu(message.message)
        cmd2 = ['rm', '/home/userf/klikbot/cookie.rar']
        system = subprocess.Popen(cmd2, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        cmd3 = ['find', '/home/userf/klikbot/cookie', '-iname', '*cookies*']
        system3 = subprocess.Popen(cmd3, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        data2 = system3.communicate()
        data3 = list(data2)
        data4 = str(data3[0:1])
        data5 = data4.split('\\')
        data66 = len(data5)
        for t in range(int(data66)):
            data61 = str(data5[t])
            data71 = data61[2:]
            if data71[0:1] == "'":
                if str(data71) == ']':
                    pass
                data81 = (str(data71[1:]))
                data91 = os.listdir(str(data81))
                data111 = len(data91)
                if len(data91) >= 0:
                    for i in range(int(data111)):
                        data101 = data81 + '/' + data91[i]
                        distanation = '/home/userf/klikbot/cookie2/cookie' + str(i)
                        shutil.move(str(data101), distanation)
            else:
                if str(data71) == ']':
                    pass
                else:
                    data81 = ('/' + str(data71))
                    data91 = os.listdir(str(data81))
                    data111 = len(data91)
                    if len(data91) >= 0:
                        for i in range(int(data111)):
                            data101 = data81 + '/' + data91[i]
                            distanation = '/home/userf/klikbot/cookie2/cookie' + str(i)
                            shutil.move(str(data101), distanation)
        shutil.rmtree('/home/userf/klikbot/cookie')    
    if message.data == 'per':
        bot.send_message(chat_id, 'Send me percents of clicks', reply_markup=keyboard2())
        dbworker.set_state(message.message.chat.id, config.States.S_ENTER_PER.value)
    if message.data == 'resetp':
        os.remove('proxy.txt')
        open("proxy.txt", "w")
        with open ('proxy.txt', 'r') as file:
                q = len(file.readlines())
        bot.send_message(chat_id, 'RESET OK! Uploaded proxy: ' + str(q) + ' pieces', reply_markup=keyboard4())        
    if message.data == 'resetc':
        files = glob.glob('/home/userf/klikbot/cookie2/*')
        for f in files:
            os.remove(f)
        cookieexists = len(os.listdir('cookie2'))
        bot.send_message(chat_id, 'RESET OK! Uploaded cookie: ' + str(cookieexists) + ' pieces', reply_markup=keyboard5())
    if message.data == 'resetch':
        os.remove('chanels')
        open("chanels", "w")
        with open ('chanels', 'r') as file:
                q = len(file.readlines())
        bot.send_message(chat_id, 'RESET OK! Uploaded channels: ' + str(q) + ' pieces', reply_markup=keyboard6())
    if message.data == 'addproxy':
        bot.send_message(chat_id, 'Send me proxy file', reply_markup=keyboard2())
        dbworker.set_state(message.message.chat.id, config.States.S_ENTER_PROXY.value)
    if message.data == 'surf':
        bot.send_message(chat_id, 'Send me SURF file!', reply_markup=keyboard2())
        dbworker.set_state(message.message.chat.id, config.States.S_ENTER_SURF.value)
    if message.data == 'addc':
        bot.send_message(chat_id, 'Send me cookie file', reply_markup=keyboard2())
        dbworker.set_state(message.message.chat.id, config.States.S_ENTER_COOKIE.value)
    if message.data == 'log':
        bot.send_message(chat_id, 'Here you can LOAD Your Log File', reply_markup=keyboard7())    
    if message.data == 'addchannel':
        bot.send_message(chat_id, 'Send me channel file', reply_markup=keyboard2())
        dbworker.set_state(message.message.chat.id, config.States.S_ENTER_CHANEL.value)
    if message.data == 'load':
        file = open('/home/userf/klikbot/LOG.txt')
        bot.send_document(chat_id, file, reply_markup=keyboard2())
@bot.message_handler(content_types='document')
def document(message):
    chat_id = message.chat.id
    state = dbworker.get_current_state(message.chat.id)
    name = message.document.file_name
    buttonz = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Back', callback_data='back')
    buttonz.add(btn1)
    buttonz2 = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Cancel', callback_data='back')
    btn2 = types.InlineKeyboardButton(text='OK', callback_data='ok')
    buttonz2.add(btn1, btn2)
    if state == config.States.S_ENTER_PROXY.value:
        raw = message.document.file_id
        name1 = 'proxy'
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(name1, 'wb') as new_file:
            new_file.write(downloaded_file)
        with open('proxy') as file:
            lines = file.readlines()
        if name[-4::] == '.txt':
            with open('proxy.txt', 'a') as file_proxy:
                file_proxy.writelines(lines)
            os.remove('proxy')
            bot.send_message(chat_id, 'All good', reply_markup=buttonz)
        else:
            bot.send_message(chat_id, 'No good, need file .TXT', reply_markup=buttonz)
            os.remove('proxy')
    if state == config.States.S_ENTER_CHANEL.value:
        raw = message.document.file_id
        name2 = 'chanels'
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(name2, 'wb') as new_file:
            new_file.write(downloaded_file)
        if name[-4::] == '.txt':
            bot.send_message(chat_id, 'All good', reply_markup=buttonz)
        else:
            bot.send_message(chat_id, 'No good, need file .TXT', reply_markup=buttonz)
            os.remove('chanels')
    if state == config.States.S_ENTER_COOKIE.value:
        raw = message.document.file_id
        name3 = 'cookie.rar'
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(name3, 'wb') as new_file:
            new_file.write(downloaded_file)
        if name[-4::] == '.rar':
            cmd = ['7z', 'x', 'cookie.rar', '-o/home/userf/klikbot/cookie']
            system = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            system.communicate()
            bot.send_message(chat_id, 'All good', reply_markup=buttonz2)  
        else:
            bot.send_message(chat_id, 'No good, need file .RAR', reply_markup=buttonz)
            os.remove('cookie.rar')
    if state == config.States.S_ENTER_SURF.value:
        raw = message.document.file_id
        name33 = 'surf'
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(name33, 'wb') as new_file:
            new_file.write(downloaded_file)
        if name[-4::] == '.txt':
            bot.send_message(chat_id, 'All good', reply_markup=buttonz)
        else:
            bot.send_message(chat_id, 'No good, need file .TXT', reply_markup=buttonz)
            os.remove('surf')
    
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_PER.value)
def percent(message):
    chat_id = message.chat.id
    text = message.text
    if text.isalpha():
        bot.send_message(chat_id, 'incorrect value', reply_markup=keyboard2())
        bot.delete_message(chat_id, message.message_id)
        return
    else:
        con = sqlite3.connect('./BotDB.db', timeout=2)
        cur = con.cursor()
        cur.execute("UPDATE settings SET percent='" + str(text) + "' ")
        con.commit()
        cur.close()
        con.close()
        bot.send_message(chat_id, 'ALL GOOD!', reply_markup=keyboard2())
        dbworker.set_state(message.chat.id, config.States.S_START.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_PERV.value)
def percent(message):
    chat_id = message.chat.id
    text = message.text
    if text.isalpha():
        bot.send_message(chat_id, 'incorrect value', reply_markup=keyboard2())
        bot.delete_message(chat_id, message.message_id)
        return
    else:
        con = sqlite3.connect('./BotDB.db', timeout=2)
        cur = con.cursor()
        cur.execute("UPDATE settings SET percentv='" + str(text) + "' ")
        con.commit()
        cur.close()
        con.close()
        bot.send_message(chat_id, 'ALL GOOD!', reply_markup=keyboard2())
        dbworker.set_state(message.chat.id, config.States.S_START.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_LEN.value)
def percent(message):
    chat_id = message.chat.id
    text = message.text
    if text.isalpha():
        bot.send_message(chat_id, 'Incorrect value!!', reply_markup=keyboard2())
        bot.delete_message(chat_id, message.message_id)
        return
    else:
        con = sqlite3.connect('./BotDB.db', timeout=2)
        cur = con.cursor()
        cur.execute("UPDATE settings SET lengh='" + str(text) + "' ")
        con.commit()
        cur.close()
        con.close()
        bot.send_message(chat_id, 'ALL GOOD!', reply_markup=keyboard2())
        dbworker.set_state(message.chat.id, config.States.S_START.value)

def keyboard():
    buttonz = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text='Upload proxy', callback_data='proxy')
    btn2 = types.InlineKeyboardButton(text='Upload channels', callback_data='channels')
    btn3 = types.InlineKeyboardButton(text='Upload Cookie', callback_data='FP')
    btn4 = types.InlineKeyboardButton(text='Upload SURF file', callback_data='surf')
    btn5 = types.InlineKeyboardButton(text='Settings', callback_data='sett')
    btn6 = types.InlineKeyboardButton(text='LOG FILE', callback_data='log')  
    btn7 = types.InlineKeyboardButton(text='START With Cookie#1', callback_data='1')
    btn8 = types.InlineKeyboardButton(text='START Without Cookie#2', callback_data='2')
    buttonz.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    return buttonz

def keyboard2():
    buttonz = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Back', callback_data='back')
    buttonz.add(btn1)
    return buttonz

def keyboard3():
    buttonz = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Percents of clicks(%)', callback_data='per')
    btn2 = types.InlineKeyboardButton(text='Percents of videos on channel(%)', callback_data='perv')
    btn3 = types.InlineKeyboardButton(text='Video lenght(sec)', callback_data='len')
    btn4 = types.InlineKeyboardButton(text='Back', callback_data='back')
    buttonz.add(btn1, btn2, btn3, btn4)
    return buttonz

def keyboard4():
    buttonz = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Reset proxy', callback_data='resetp')
    btn2 = types.InlineKeyboardButton(text='Add file proxy', callback_data='addproxy')
    btn3 = types.InlineKeyboardButton(text='Back', callback_data='back')
    buttonz.add(btn1, btn2, btn3)
    return buttonz

def keyboard5():
    buttonz = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Reset cookie', callback_data='resetc')
    btn2 = types.InlineKeyboardButton(text='Add file cookie', callback_data='addc')
    btn3 = types.InlineKeyboardButton(text='Back', callback_data='back')
    buttonz.add(btn1, btn2, btn3)
    return buttonz

def keyboard6():
    buttonz = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Reset channels', callback_data='resetch')
    btn2 = types.InlineKeyboardButton(text='Add file channels', callback_data='addchannel')
    btn3 = types.InlineKeyboardButton(text='Back', callback_data='back')
    buttonz.add(btn1, btn2, btn3)
    return buttonz

def keyboard7():
    buttonz = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Back', callback_data='back')
    btn2 = types.InlineKeyboardButton(text='Load LOG', callback_data='load')
    buttonz.add(btn1, btn2)
    return buttonz

def keyboard8():
    buttonz = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Start', callback_data='start')
    btn2 = types.InlineKeyboardButton(text='Stop', callback_data='stop')
    btn3 = types.InlineKeyboardButton(text='Back', callback_data='back')
    buttonz.add(btn1, btn2, btn3)
    return buttonz

bot.polling(none_stop=True)
from config import Config
import os,certifi
from pyrogram import Client,errors
import telebot
import threading
from telebot import types
import asyncio
from backend import app
from db import database

DB = database()
App = app()
os.environ['SSL_CERT_FILE'] = certifi.where() 
api_id = Config.APP_ID
api_hash = Config.API_HASH
TELEGRAM_TOKEN=Config.TG_BOT_TOKEN
bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False,num_threads=55,skip_pending=True)
@bot.message_handler(commands=['start'])
def Admin(message):
    AddAccount=types.InlineKeyboardButton("• ئەکاونتێک زیاد بکە •",callback_data="AddAccount")
    Accounts=types.InlineKeyboardButton("",callback_data="Accounts")
    a1=types.InlineKeyboardButton("• گواستنەوە ئەندامەکان •",callback_data="a1")
    inline = types.InlineKeyboardMarkup(keyboard=[[a1],[AddAccount],[Accounts]])
    bot.send_message(message.chat.id,"""*بەخێرهاتی ئازیزم  👋
    
لە دوگمەکانی خوارەوە ئەوەی دەتەوێت هەڵبژێرە
دەتوانیت ئەندامەکان بگوازیتەوە بۆ گروپەکەت 
لەهەر گروپیکی ترەوە بێت 👤
 *""",reply_markup=inline ,parse_mode="markdown")

@bot.callback_query_handler(lambda call:True)
def call(call):
    if call.data =="Accounts":
        num = DB.accounts()
        msg=bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=f"ئەکاونتە تەواو تۆمارکراوەکانتان 📋 : {num}",parse_mode="markdown")
    if call.data =="AddAccount":
        msg=bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="*ئێستا ئەو ژمارەیەی دەتەوێت بیگەیەنیت بە کۆدی وڵاتەوە بنێرە : نموونە +964 775 106 4027*📞",parse_mode="markdown")
        bot.register_next_step_handler(msg, AddAccount)
    if call.data =="a1":
        msg=bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="*لینکی ئەو گروپە بنێرە کە دەتەوێت لێیەوە بگوازیتەوە *🖲",parse_mode="markdown")
        bot.register_next_step_handler(msg, statement)
def statement(message):
    Fromgrob = message.text
    msg =bot.send_message(chat_id=message.chat.id,text="*لینکی ئەو گروپە بنێرە کە دەتەوێت بیگوازیتەوە بۆی*🧲",parse_mode="markdown")
    bot.register_next_step_handler(msg, statement2,Fromgrob)
def statement2(message,Fromgrob):
    Ingrob = message.text
    msg=bot.send_message(chat_id=message.chat.id,text="*کەمێک چاوەڕوان بن ⏱*",parse_mode="markdown")
    T = threading.Thread(target=asyncio.run,args=(App.GETuser(Fromgrob,Ingrob),))
    T.start()
    T.join()
    list = T.return_value
    numUser = len(list)
    bot.send_message(message.chat.id,f"""*هەموو ئەندامە بەردەستەکان بە سەرکەوتوویی پاشەکەوت کراون *✅

*زانیاری گواستنەوە 🗒️

 ئەندامانی بەردەست : {numUser} ئەندام 👤
گواستنەوە لە : {Fromgrob} 🎒
گواستنەوە بۆ : {Ingrob} 🧳
ماوەی تاقیکردنەوە : 1 جرکە ⏱

چاوەڕێ بکە تا پرۆسەکە تەواو دەبێت ♻️* """ ,parse_mode="markdown")
    T = threading.Thread(target=asyncio.run,args=(App.ADDuser(list,Ingrob,message.chat.id,bot),))
    T.start()
def AddAccount(message):
    try:         
        if "+" in message.text:
            bot.send_message(message.chat.id,"*چاوەڕێ بکە لەکاتی سکانکردندا* ⏱",parse_mode="markdown")
            _client = Client("::memory::", in_memory=True,api_id=api_id, api_hash=api_hash,lang_code="ar")
            _client.connect()
            SendCode = _client.send_code(message.text)
            Mas = bot.send_message(message.chat.id,"*ئەو کۆدە لێرە داخڵ بکە کە بۆت نێردراوە نموونە : 9 6 7 1 6 پیویستە بۆشای لە نێوان ژمارەکان بکەیت 🔏*",parse_mode="markdown")
            bot.register_next_step_handler(Mas, sigin_up,_client,message.text,SendCode.phone_code_hash,message.text)	
        else:
            Mas = bot.send_message(message.chat.id,"*چاوەڕێ بکە لەکاتی سکانکردندا* ⏱")
    except Exception as e:
        bot.send_message(message.chat.id,"ERORR : "+e)
def sigin_up(message,_client,phone,hash,name):
    try:
        bot.send_message(message.chat.id,"*کەمێک چاوەڕوان بن ⏱*",parse_mode="markdown")
        _client.sign_in(phone, hash, message.text)
        bot.send_message(message.chat.id,"*ئەکاونتەکە بە سەرکەوتوویی پشتڕاست کراوەتەوە ✅ *",parse_mode="markdown")
        ses= _client.export_session_string()
        DB.AddAcount(ses,name,message.chat.id)
    except errors.SessionPasswordNeeded:
        Mas = bot.send_message(message.chat.id,"*وشەی نهێنی ئەکاونتەکەت دابنێ 🔐*",parse_mode="markdown")
        bot.register_next_step_handler(Mas, AddPassword,_client,name)	
def AddPassword(message,_client,name):
    try:
        _client.check_password(message.text) 
        ses= _client.export_session_string()
        DB.AddAcount(ses,name,message.chat.id)
        try:
            _client.stop()
        except:
            pass
        bot.send_message(message.chat.id,"*ئەکاونتەکە بە سەرکەوتوویی پشتڕاست کراوەتەوە ✅ *",parse_mode="markdown")
    except Exception as e:
        print(e)
        try:
            _client.stop()
        except:
            pass
        bot.send_message(message.chat.id,f"ERORR : {e} ")
bot.infinity_polling(none_stop=True,timeout=15, long_polling_timeout =15)

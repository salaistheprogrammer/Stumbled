import telegram
import sqlite3
import random
import datetime
import traceback
from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
from typing import Final
from time import sleep
from pathlib import Path


TOKEN: Final = '6385414066:AAF5_qzeXOp94f09ID9uBXoH82Y056ARWS8'
BOT_USERNAME: Final = "ThoughtsManagerBot"


updater = telegram.ext.Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

#to write execution func for repeating sql commands

def check_for_user(update: Update, context: CallbackContext, cid):
    # "C:\\Projects\\Tele-bot\\stbot.db"
    con = sqlite3.connect(Path(__file__).parent / 'stbot.db')
    c = con.cursor()

    c.execute('select cid from cids')
    status = c.fetchall()

    if (cid, ) not in status:
        c.execute('insert into cids (cid) values (?)', (cid, ))
        context.bot.send_message(chat_id=cid, text=f"Hi {update.effective_chat.first_name}, Stumble here(pun intended), I help you not stumble over thoughts. Looks like you're new here.")
        context.bot.send_message(chat_id=cid, text="By the way, I'll help you manage your thoughts. You may add your thoughts using the /add command.")
        context.bot.send_message(chat_id=cid, text="To know how I do what I do to help you with your thoughts, you shall use the /help command.")
        con.commit()
    
    else:
        context.bot.send_message(chat_id=cid, text=f'Hi {update.effective_chat.first_name}, Stumble here.')

    c.close()
    con.close()

    
def start(update: Update, context: CallbackContext):

    cid = update.effective_chat.id
    check_for_user(update, context, cid)

    
def add(update: Update, context: CallbackContext):

    cid = update.effective_chat.id
    addition = update.message.text[5: ]

    con = sqlite3.connect('stbot.db')
    c = con.cursor()

    c.execute('insert into stumbles (cid, stumbles) values (?, ?)', (cid, addition))
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'ADDED: {addition}')

    con.commit()
    c.close()
    con.close()

#new
def daily_stumble(update: Update, context: CallbackContext):

    cid = update.effective_chat.id
    daily = update.message.text[7: ]

    con = sqlite3.connect('stbot.db')
    c = con.cursor()

    c.execute('insert into stumbles (cid, daily) values (?, ?)', (cid, daily))

    context.bot.send_message(chat_id=cid, text=f"ADDED '{daily}' to daily stumbles.")

    con.commit()
    c.close()
    con.close()

def delete(update: Update, context: CallbackContext):

    deletion = update.message.text[8: ]
    
    con = sqlite3.connect('stbot.db')
    c = con.cursor()

    c.execute(f"select stumbles from stumbles where cid = ?", (update.effective_chat.id,))
    stumbles = c.fetchall()

    for stumble in stumbles:

        # print(stumble[0], deletion , type(stumble[0]), type(deletion))
        if stumble[0] == deletion:
            c.execute('delete from stumbles where stumbles = ?', (deletion,))
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'DELETED: {deletion}')
            break
        
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"'{deletion}' does not already exist in your stumbles. To know the thoughts you've added, send /list command.")

    con.commit()
    c.close()
    con.close()


def list(update: Update, context: CallbackContext):

    cid = update.effective_chat.id

    con = sqlite3.connect('stbot.db')
    c = con.cursor()

    c.execute('select stumbles from stumbles where cid = ?', (cid, ))
    stumbles = c.fetchall()
    st_list = []

    for stumble in stumbles:
        st_list.append(stumble[0])

    context.bot.send_message(chat_id=cid, text=f"{enumerate(st_list, 1)}")
    

def sender():

    # print('sent')
    con = sqlite3.connect('stbot.db')
    c = con.cursor()

    c.execute('select cid from cids')
    cids = c.fetchall()

    bot = Bot(token="6385414066:AAF5_qzeXOp94f09ID9uBXoH82Y056ARWS8")

    for cid in cids:

        c.execute('select stumbles from stumbles where cid = ?', cid)
        stumbles = c.fetchall()
        #new
        c.execute('select daily from stumbles where cid = ?', cid)
        daily = c.fetchone()

        msg = random.choice(stumbles)

        bot.send_message(chat_id=cid[0], text=msg[0])
        #new
        bot.send_message(chat_id=cid[0], text=daily[0]) if daily else None

        
def error_handler(update: Update, context: CallbackContext):

    print("An error occurred:", context.error)
    traceback.print_exc()
    context.bot.send_message(chat_id=5360161813, text=f"{context.error}")



def send_on_time(func, send_time): 
 
    while True:

        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        sleep(1)

        if current_time == send_time:
            func()


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('add', add))
dispatcher.add_handler(CommandHandler('delete', delete))
dispatcher.add_handler(CommandHandler('list', list))
dispatcher.add_handler(CommandHandler('daily', daily_stumble))
dispatcher.add_error_handler(error_handler)

updater.start_polling()

send_time = "10:00:00 AM"
send_on_time(sender, send_time)
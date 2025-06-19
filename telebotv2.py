import telegram.ext
import sqlite3
import random
import datetime
import traceback
from telegram import Bot
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import Update
from typing import Final
from time import sleep


TOKEN: Final = "Bot's token"
BOT_USERNAME: Final = "Bot's Username"


updater = telegram.ext.Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher


#to write execution func for repeating sql commands

def check_for_user(update: Update, context: CallbackContext, cid):

    con = sqlite3.connect('stbot.db')
    c = con.cursor()

    c.execute('select cid from cids')
    status = c.fetchall()

    if (cid, ) not in status:
        c.execute('insert into cids (cid) values (?)', (cid,))
        context.bot.send_message(chat_id=cid, text="Hi, Stumbled here. Looks like you're new here.")
        context.bot.send_message(chat_id=cid, text="By the way, I'll help you manage your thoughts. You may add your thoughts using the /add command.")
        context.bot.send_message(chat_id=cid, text='''
Here are the commands that you'll get to use here:

Commands:

    /add - Lets you add your thoughts to the database.
    /delete - Lets you delete the thought you specified from the database.
    /list - Sends a list of your thoughts.
    /howitworks - Explains you how the bot works.

Usage of those commands:

    /add Thought you want to add
    /delete Thought you want to delete
    /list [no arguments]
    /help [no arguments]
    /howitworks [no arguments]''')

        con.commit()

    else:
        context.bot.send_message(chat_id=cid, text='Hi, Stumbled here.')

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


def delete(update: Update, context: CallbackContext):

    deletion = update.message.text[8: ]

    con = sqlite3.connect('stbot.db')
    c = con.cursor()

    c.execute("select stumbles from stumbles where cid = ?", (update.effective_chat.id,))
    stumbles = c.fetchall()

    for stumble in stumbles:

        # print(stumble[0], deletion , type(stumble[0]), type(deletion))

        if stumble[0] == deletion:
            c.execute('delete from stumbles where stumbles = ?', (deletion,))
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'DELETED: {deletion}')
            break

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"'{deletion}' does not already exist in your stumbles(thoughts). To know the thoughts you've added, send /list command.")

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

    for num, stumble in enumerate(stumbles, start=1):
        st_list.append((num, stumble))

    # for stumble in stumbles:
    #     st_list.append(stumble[0])

    context.bot.send_message(chat_id=cid, text=f"{st_list}")


def help(update: Update, context):

    context.bot.send_message(chat_id=update.effective_chat.id,
    text='''
Commands:

    /add - Lets you add your thoughts to the database.
    /delete - Lets you delete the thought you specified from the database.
    /list - Sends a list of your thoughts.
    /howitworks - Explains you how the bot works.

Usage of those commands:

    /add Thought you want to add
    /delete Thought you want to delete
    /list [no arguments]
    /help [no arguments]
    /howitworks [no arguments]''')


def howitworks(update: Update, context):

    cid = update.effective_chat.id
    text = '''Say you watch movies, read books and listen to songs. You may find inspirations from all of those. That may be a quote, a dialouge or a lyrical line. As you consume a lot of those, you'll forget a lot of those too.
Espeacially after reading a book, self-reflecting the contents that you read is very important to learn. Some of them can teach you new things every time you self-reflect them. And that's where I'll help you. If you
add those thoughts to my database using the /add command, I'll send you one thought per day. So you could learn the most out of everything you are exposed to. Once yoou add 10 or more than 10 thoughts, I'll start sending them.'''

    context.bot.send_message(chat_id=cid, text=text)


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

        if len(stumbles) >= 10:

            msg = random.choice(stumbles)
            bot.send_message(chat_id=cid[0], text=msg[0])


def error_handler(update: Update, context: CallbackContext):

    print("An error occurred:", context.error)
    traceback.print_exc()
    context.bot.send_message(chat_id=5360161813, text=f'An error occured: {context.error}')


def send_on_time(func, send_time):

    while True:

        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        sleep(1)
        # print(current_time, current_time == send_time)

        if current_time == send_time:
            func()


def message_handler(update: Update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="I don't understand messages. Please use the predefined commands.")


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('add', add))
dispatcher.add_handler(CommandHandler('delete', delete))
dispatcher.add_handler(CommandHandler('list', list))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('howitworks', howitworks))
dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
dispatcher.add_error_handler(error_handler)

updater.start_polling()

send_time = "04:30:00 AM"
send_on_time(sender, send_time)

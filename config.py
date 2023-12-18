from pyrogram import Client,MessageHandler
#from pyrogram.handlers import MessageHandler
import datetime
import sqlite3
import textdistance


global fromchannel, tochannel
#import requests
#api_id = input("insert api id of bot")
api_id = input("input api id bot : ")
api_hash = input("input api hash bot :")
app = Client(
    "my_accouchatnt",
    api_id= api_id,
    api_hash= str (api_hash)
)
databaseidname = 'databaseid.db'


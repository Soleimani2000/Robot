from config import *
import config
def createdb():
    conn = sqlite3.connect(config.databaseidname)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS token (id   integer PRIMARY KEY)''')


def insertdb(id):
    conn = sqlite3.connect(config.databaseidname)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO token VALUES (?)', (id,))
    conn.commit()
    conn.close()


def cheackdb(id):
    conn = sqlite3.connect(conig.databaseidname)
    c = conn.cursor()
    c.execute("""SELECT id FROM token WHERE id=? """, (id,))
    result = c.fetchone()
    if not result:
        return True
    return None


def db(token, text):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS message (token TEXT NOT NULL, text TEXT NOT NULL,  PRIMARY KEY (token))""")
    c.execute("""SELECT token FROM message WHERE token=? """, (token, ))
    result = c.fetchone()
    if not result:
        c.execute('INSERT OR IGNORE INTO message VALUES (?, ?)', (token, text ))
        conn.commit()
        conn.close()
        return True
    conn.commit()
    conn.close()
    return None


def similarity(text):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""SELECT text FROM message WHERE 1 LIMIT 80 """)
    results = c.fetchone()
    for item in results:
        tokens_1 = item.split()
        tokens_2 = text.split()
        similar = textdistance.jaccard(tokens_1, tokens_2)
        if similar > 0.6:
            return False
        else:
            return True
file1 = open('from.txt', 'r')
fromchannel = file1.read().splitlines()
file2 = open('to.txt', 'r')
tochannel = file2.read().splitlines()
createdb()
global list
list = []


def sender(client, message):
    global fromchannel, tochannel, list
    type = message.chat.type
    if type in ['channel','supergroup' , 'group'] and message.chat.id not in list:
        print(message.chat.id , " ", message.chat.title)
        list.append(message.chat.id)
    if type == 'channel':
            #print(message)
            number = 0
            try:
                index = fromchannel.index(message.chat.username)
            except:
                index = None
            if index != None:
                    if message.text != None:
                        check = db(message.message_id, message.text)
                        if  check == True:
                            status = similarity(message.text)
                            if status:
                                message.forward(tochannel[index])
                                insertdb(message.message_id)
                                pass
                            else:
                                print("repeat text " )
                    else:
                        message.forward(tochannel[index])
                        insertdb(message.message_id)

                    #print("send medssage from ", source, " to ", tochannel[number])


    elif type == 'supergroup':
        flag = False
        if message.chat.username in fromchannel or str(message.chat.id) in fromchannel:
            flag = True
        if flag:
            index = None
            try:
                index = fromchannel.index(message.chat.username)
            except:
                index = fromchannel.index(str(message.chat.id))
            if(index != None):
                if (message.forward_from) != None:
                    for source in fromchannel:
                            messageid = message.message_id
                            cheack = cheackdb(message.message_id)
                            if cheack:
                                message.forward(fromchannel[index])
                                insertdb(message.message_id)

                else:
                    if message.photo:
                        cheack = cheackdb(message.message_id)
                        if cheack and message.caption != None:
                            message.forward(tochannel[index])
                            insertdb(message.message_id)
                    elif message.video:
                        cheack = cheackdb(message.message_id)
                        if cheack:
                            message.forward(tochannel[index])
                            insertdb(message.message_id)
                        elif message.animation:
                            cheack = cheackdb(message.message_id)
                            if cheack:
                                message.forward(tochannel[index])
                                insertdb(message.message_id)

    elif type == 'group':
        flag = False
        if message.chat.username in fromchannel or str(message.chat.id) in fromchannel:
            flag = True
        if flag:
            index = None
            try:
                index = fromchannel.index(message.chat.username)
            except:
                index = fromchannel.index(str(message.chat.id))
            if (index != None):
                if (message.forward_from) != None:
                        cheack = cheackdb(message.message_id)
                        if cheack:
                            message.forward(tochannel[index])
                            insertdb(message.message_id)
                else:
                    if message.photo:
                        cheack = cheackdb(message.message_id)
                        if cheack and message.caption != None:
                            message.forward(tochannel[index])
                            insertdb(message.message_id)
                    elif message.video:
                        cheack = cheackdb(message.message_id)
                        if cheack:
                            message.forward(tochannel[index])
                            insertdb(message.message_id)
                    elif message.animation:
                        cheack = cheackdb(message.message_id)
                        if cheack:
                            message.forward(tochannel[index])
                            insertdb(message.message_id)



my_handler = MessageHandler(sender)
app.add_handler(my_handler)
app.run()


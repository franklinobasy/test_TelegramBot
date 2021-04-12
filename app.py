from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name, URL
import re

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token = TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    #receive the message in JSON and then transform it to telegram object
    update = telegram.Update.de_json(request.get_json(force= True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    #Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()

    #for debugging purposes only
    print('got text message: ', text)

    #The first time you chat with the bot AKA welcome message
    if text == '/start':
        #print welcome message
        bot_message = '''
        Welcome to EnuchiBot, the bot is using the service from http://avatars.adorable.io/ to generate cool looking avatars 
        based on the name you entered. So please enter a name and the bot will reply with an avatar for your name.
        '''

        #send the welcoming message
        bot.sendMessage(chat_id = chat_id, text = bot_message, reply_to_message_id = msg_id)

    else:
        try:
            #clear the message we got from any non alphabets
            text = re.sub(r"\W", "_", text)
            
            #create the api link of the avatar based on http://avatars.adorable.io/
            url = "http://api.adorable.io/avatars/285/{}.png".format(text.strip())

            #reply with a photo to the name the user sent
            #note that you can send photos by url and telegram will fetch it for you
            bot.sendPhoto(chat_id= chat_id, photo=url, reply_to_message_id= msg_id)
        except Exception:
            #if things went wrong
            error_text = "There was a problem with the name you used, please enter different name"
            bot.sendMessage(chat_id= chat_id, text= error_text, reply_to_message_id= msg_id)

    return "OK"

@app.route('/setwebhook', methods= ['GET', 'POST'])
def set_webhook():
    #we use the bot object to link the bot to our app which live

    # in the link provided by the URL
    s = bot.setWebhook('{URL} {HOOK}'.format(URL= URL, HOOK= TOKEN))

    #something to let us know if it works fine
    if s:
        return 'webhook setup is OK'
    else:
        return 'webhook setup failed'

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    #threaded arg allow your app to have more than one thread
    app.run(threaded= True)
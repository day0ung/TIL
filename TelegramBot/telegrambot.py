import telegram  # pip install python-telegram-bot


BOT_TOKEN = "5829966076:AAFG4-boVEJi6Bq1Ar7G35yJAHFDS83KTeQ"
CHAT_ID = "-717449850"
bot = telegram.Bot(BOT_TOKEN)

def send_msg():
    msg = 'hi'
    bot.sendMessage(chat_id=CHAT_ID, text=msg)

if __name__ == '__main__':
    send_msg()
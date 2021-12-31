import logging
import time

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, message
import user as user
updater = Updater(token="TOKEN", use_context=True)
dispatcher = updater.dispatcher
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
from bs4 import BeautifulSoup
import requests


items = []


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def hello(update, context):
    """Send a message when the command /start is issued."""
    user = str(update.effective_user.first_name)
    first_letter = user[0:1].upper()
    full_name = user[1:-1]
    last_letter = user[-1]
    user = first_letter + full_name + last_letter
    update.message.reply_text(f"Hello {user}, I'm yours to command.\nPress /start to use me.")



def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Select /search word to search words on oxford dictionary\nSelect /view word to see words you have searched\nSelect /hello to greet me')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Press /start to use this bot!")

def error(update, context, logger):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def search (update, context):
    # List of items that users want to monitor
    item = update.message.text
    item= item[8:]
    base_url = "https://www.thefreedictionary.com/"
    split = item.strip().split(' ')
    if len(split) > 1 or split == ['']:
        update.message.reply_text("Sorry, I can only accept one word as argument [e.g /search water]")
    else:
        items.append(item)
        link = base_url + item
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, "html.parser")
            definition = soup.find("div", {"class":"ds-list"})
            definition = definition.text
            definition = str(definition)[2:]
            update.message.reply_text(definition)

        except Exception as e:
            print(e)
            update.message.reply_text("Sorry I'm unable to search for the definition of this word")



def view (update, context):
    for count, item in enumerate(items, 1):
        update.message.reply_text(f"{count}. {item}")



def manage_command(update, context):
    update.message.reply_text("Unknown command. Press /help for more info")

def manage_text(update, context):
    update.message.reply_text("Unknown command. Press /help for more info")




def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary


    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("hello", hello))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(CommandHandler("view", view))


    dp.add_handler(MessageHandler(Filters.command, manage_command))
    dp.add_handler(MessageHandler(Filters.text, manage_text))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()

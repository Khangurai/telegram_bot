# from telegram import Bot, Update
# from telegram.ext import CommandHandler, Updater
#
# TOKEN = '7250327428:AAG-L1s668fO1vp8_dunBfXYDmOvwO-Lywo'
#
# # Command handler for /start command
# def start(update: Update, context):
#     update.message.reply_text('Bot is online and ready!')
#
# # Custom command to check bot status
# def check_status(update: Update, context):
#     bot = context.bot
#     try:
#         bot.get_me()  # Attempt to get bot information
#         update.message.reply_text('Bot is online and responsive!')
#     except Exception as e:
#         print(f'Bot is offline: {e}')
#         update.message.reply_text('Warning: Bot is currently offline!')
#
# def main():
#     updater = Updater(token=TOKEN, use_context=True)
#     dispatcher = updater.dispatcher
#
#     # Command handlers
#     dispatcher.add_handler(CommandHandler("start", start))
#     dispatcher.add_handler(CommandHandler("check_status", check_status))
#
#     updater.start_polling()
#     updater.idle()
# if __name__ == '__main__':
#     main()


from telegram.ext import Updater, CommandHandler

TOKEN = '6267551636:AAHh__xd8O-dABF9gjMzlbuo5At5nazGmGA'

# Command handler for /start command
def start(update, context):
    update.message.reply_text('Bot is online and ready!')

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

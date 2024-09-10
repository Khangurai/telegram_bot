from typing import Final
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputFile
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from user_data import VALID_USERS  # Importing user data from another file

# Constants
TOKEN: Final = '7250327428:AAFie1LByPvklyk6Py4Hrv5WY6QfDCtyvz0'
BOT_USERNAME: Final = '@yourbotusername'

# States for the conversation handler
SELECT_NAME, GET_ID = range(2)

# # Flag for maintenance mode
# is_under_maintenance = True
# Global variable for maintenance mode
MAINTENANCE_MODE: bool = False  # Set to True to enable maintenance mode

# Command handler for the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if MAINTENANCE_MODE:
        message = (
            "```\n"
            "🚧 Server Maintenanceပြုလုပ်နေပါသဖြင့် Services များအသုံးပြုလို့မရသေးပါ \n\n"
            "```\n"
        )
        photo = 'https://t.me/ownproject711/47'
        caption = 'Server Maintenance in Progress'
        #await update.message.reply_text('🚧 All services are currently unavailable due to maintenance. Please try again later.')
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN_V2)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=caption)
        return

# Command handler for the /start command
# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Greeting message with instructions
    message = (
        "*မင်္ဂလာပါ 👋*\n"
        "ကျွန်တော်က V2ray server ထုတ်ပေးနိုင်တဲ့စက်ရုပ်လေးပါ 🤖\n"
        "အောက်ကအဆင့်လေးတွေကို လုပ်ပြီး server ပြန်ယူနိုင်ပါတယ်\n\n"
        "```\n"
        "menu ကိုသွားပါ\n"
        "```\n"
        "```\n"
        "'ကုတ်ထုတ်ရန်' ကိုရွေးပေးပါ✅\n"
        "```\n"
        # "```\n"
        # "V2box Device ID လေးထည့်ပြီး Server ပြန်ထုတ်ယူနိုင်ပါပြီ 💜\n\n"
        # "```\n"
        "ကျွန်တော့်ကို [Aung Kaung Khant](tg://user?id=5897565175) ကဖန်တီးထားတာပါ 🥷\n\n"
    )
    #video_url = 'https://t.me/ownproject711/46'

    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN_V2)
    #await context.bot.send_video(chat_id=update.effective_chat.id, video=video_url,
       #                          caption="အသုံးပြုနည်းvideo ကြည့်မလား?")

# Command handler for the /generatev2ray command
async def generatev2ray_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if MAINTENANCE_MODE:
        message = (
            "```\n"
            "🚧 Server Maintenanceပြုလုပ်နေပါသဖြင့် Services များအသုံးပြုလို့မရသေးပါ \n\n"
            "```\n"
        )
        photo = 'https://t.me/ownproject711/47'
        caption = 'Server Maintenance in Progress'
        #await update.message.reply_text('🚧 All services are currently unavailable due to maintenance. Please try again later.')
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN_V2)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=caption)
        return
    message = (
        "V2ray serverများရယူနိုင်ရန် ဒီ[channel](https://t.me/+xTZktPqi3M9mZjQ9) ကိုjoinပေးပါ 🥷\n\n"
        "'နောက်ပိုင်းဒီ [channel](https://t.me/+xTZktPqi3M9mZjQ9) ထဲမှာပဲ့ announcement လုပ်ပေးပါမယ် 💜'\n\n"
    )
    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN_V2)


# Function to handle user messages
def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'hello' in processed:
        return 'Hey there'
    if 'help' in processed:
        return 'What can you do?'
    return 'လုပ်ဆောင်ချက်မှားနေပါတယ်'


# Handler for general text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)


# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Main function to start the bot
if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).read_timeout(30).build()

    # Conversation handler for generating V2Ray links
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('generatev2ray', generatev2ray_command)],
        states={
            #SELECT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_name)],
            #GET_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_id)]
        },
        fallbacks=[],
    )

    # Add handlers to the application
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('start', start_command))
    #app.add_handler(CommandHandler('vpnbuy', vpnbuy_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)

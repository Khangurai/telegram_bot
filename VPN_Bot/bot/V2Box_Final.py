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
        "'ကုတ်ထုတ်ရန်' ကိုရွေးပြီး username ရွေးပေးပါ✅\n"
        "```\n"
        "```\n"
        "V2box Device ID လေးထည့်ပြီး Server ပြန်ထုတ်ယူနိုင်ပါပြီ 💜\n\n"
        "```\n"
        "ကျွန်တော့်ကို [Aung Kaung Khant](tg://user?id=5897565175) ကဖန်တီးထားတာပါ 🥷\n\n"
        "```\n"
        "*အခုကတော့ DEMO version လေးပါ နောက်နှစ်ရက်ကြာရင် usernameအစုံရပြီနော်*"
        "```\n"
    )
    video_url = 'https://t.me/ownproject711/46'

    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN_V2)
    await context.bot.send_video(chat_id=update.effective_chat.id, video=video_url,
                                 caption="အသုံးပြုနည်းvideo ကြည့်မလား?")

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
    # Ask the user to select a name from available users
    reply_keyboard = [[info['name']] for info in VALID_USERS.values()]
    await update.message.reply_text(
        'နာမည်ရွေးပေးပါဦး:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return SELECT_NAME


# Handler for the SELECT_NAME state
async def select_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    selected_name = update.message.text

    # Find the selected user by name
    user_id = next((uid for uid, info in VALID_USERS.items() if info['name'] == selected_name), None)
    if not user_id:
        # If the selected name is invalid, prompt the user to select again
        await update.message.reply_text('Invalid name selected. Please try again.')
        return SELECT_NAME

    print(f"{user.first_name} selected name: {selected_name}")

    # Prompt the user to enter their V2Box ID
    await update.message.reply_text(
        'V2Box ရဲ့ Device ID ကိုရိုက်ထည့်ပေးပါ:',
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data['user_id'] = user_id  # Store the user ID in the context
    context.user_data['selected_name'] = selected_name  # Store the selected name in the context
    return GET_ID  # Move to the GET_ID state


# Handler for the GET_ID state
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = context.user_data.get('user_id')
    selected_name = context.user_data.get('selected_name')
    entered_id = update.message.text

    # Check if entered ID matches user's ID
    if entered_id == user_id:
        v2ray_link = VALID_USERS[user_id]['v2raylink']
        formatted_message = (
            "*Server ကို copy ယူပြီး V2Box ထဲမှာပြန်သုံးနိုင်ပါတယ်*\n"
            "```\n"
            f"{selected_name} Server:\n"  # This line will appear as code without a copy button if it's short
            "```\n"
            "```\n"
            f"{v2ray_link}\n"  # This line will appear as code
            "```\n"
        )
        await update.message.reply_text(formatted_message, parse_mode=ParseMode.MARKDOWN_V2)
        # Reset user data for next usage
        context.user_data.clear()
        return ConversationHandler.END
    else:
        # Increment incorrect attempt count
        if 'attempt' not in context.user_data:
            context.user_data['attempt'] = 1
        else:
            context.user_data['attempt'] += 1

        # Check if exceeded maximum attempts
        if context.user_data['attempt'] >= 3:
            await update.message.reply_text(
                '"ID ထည့်တာမအောင်မြင်ပါ" \n<b>Username ကိုမှန်ကန်စွာပြန်ရွေးချယ်ပေးပါ</b>:',
                reply_markup=ReplyKeyboardMarkup([[info['name']] for info in VALID_USERS.values()],
                                                 one_time_keyboard=True),
                parse_mode=ParseMode.HTML
            )
            # Reset user data for next usage
            context.user_data.clear()
            return SELECT_NAME
        else:
            await update.message.reply_text(
                f'<b>"ID မှားနေပါတယ်"</b>\nID ပြန်ရိုက်ပေးပါ ကြိုးစားရန် {3 - context.user_data["attempt"]} ကြိမ်ကျန်',
                reply_markup=ReplyKeyboardRemove(),
                parse_mode=ParseMode.HTML
            )
            return GET_ID


# Command handler for a custom command (example)
async def vpnbuy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if MAINTENANCE_MODE:
        message = (
            "```\n"
            "🚧 Server Maintenanceပြုလုပ်နေပါသဖြင့် Services များအသုံးပြုလို့မရသေးပါ \n\n"
            "```\n"
         )
    #     photo = 'https://t.me/ownproject711/47'
    #     caption = 'Server Maintenance in Progress'
     #     await update.message.reply_text(းပါ')
    #     await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN_V2)
    #     await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=caption)
    #     return
    # photo = 'https://t.me/ownproject711/48'
    message = (
          "🚧 services မရရှိနိုင်သေးပါ"
    #     "*VPNဝယ်ယူလိုပါက [Aung Kaung Khant](tg://user?id=5897565175) ကိုနှိပ်ပြီး\nဝယ်မယ့် packageကိုပို့ထားပေးပါ*\n"
    )

    # caption = 'VPN ဈေးနှုန်း'
    # await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=caption)
    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN_V2)
    return


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
            SELECT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_name)],
            GET_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_id)]
        },
        fallbacks=[],
    )

    # Add handlers to the application
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('vpnbuy', vpnbuy_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)

# from typing import Final, Tuple
# from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
# from user_data import VALID_USERS  # Importing user data from another file
#
# # Constants
# TOKEN: Final = '7250327428:AAEX0bqKJ_dHN3o1XtkCoyZQJ6pHjtpQbdA'
# BOT_USERNAME: Final = '@yourbotusername'
#
# # States
# SELECT_NAME, GET_ID = range(2)
#
# # Command Handlers
# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text('Hello! VPN users')
#
# async def generatev2ray_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # Ask the user to select a name from available users
#     reply_keyboard = [[info['name']] for info in VALID_USERS.values()]
#     await update.message.reply_text(
#         'Select a name:',
#         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
#     )
#     return SELECT_NAME
#
# async def select_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.message.from_user
#     selected_name = update.message.text
#
#     # Find the selected user by name
#     user_id = next((uid for uid, info in VALID_USERS.items() if info['name'] == selected_name), None)
#     if not user_id:
#         await update.message.reply_text('Invalid name selected. Please try again.')
#         return SELECT_NAME
#
#     print(f"{user.first_name} selected name: {selected_name}")
#
#     await update.message.reply_text(
#         'Please enter your ID:',
#         reply_markup=ReplyKeyboardRemove()
#     )
#     context.user_data['user_id'] = user_id
#     return GET_ID
#
#
# async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = context.user_data.get('user_id')
#     entered_id = update.message.text
#
#     # Check if entered ID matches user's ID
#     if entered_id == user_id:
#         v2ray_link = VALID_USERS[user_id]['v2raylink']
#         await update.message.reply_text(f"Here is your V2Ray link: {v2ray_link}")
#         return ConversationHandler.END
#     else:
#         # Increment incorrect attempt count
#         if 'attempt' not in context.user_data:
#             context.user_data['attempt'] = 1
#         else:
#             context.user_data['attempt'] += 1
#
#         # Check if exceeded maximum attempts
#         if context.user_data['attempt'] >= 3:
#             await update.message.reply_text('Maximum attempts exceeded. Please select a name again:',
#                                             reply_markup=ReplyKeyboardMarkup(
#                                                 [[info['name']] for info in VALID_USERS.values()],
#                                                 one_time_keyboard=True))
#             return SELECT_NAME
#         else:
#             await update.message.reply_text(f'Invalid ID! Please enter your ID again. '
#                                             f'Attempts remaining: {3 - context.user_data["attempt"]}',
#                                             reply_markup=ReplyKeyboardRemove())
#             return GET_ID
#
#
# async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text('This is a custom command')
#
# # Message Handlers
# def handle_response(text: str) -> str:
#     processed: str = text.lower()
#     if 'hello' in processed:
#         return 'Hey there'
#     if 'help' in processed:
#         return 'What can you do?'
#     return 'Invalid command'
#
# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     message_type: str = update.message.chat.type
#     text: str = update.message.text
#
#     print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
#
#     if message_type == 'group':
#         if BOT_USERNAME in text:
#             new_text: str = text.replace(BOT_USERNAME, '').strip()
#             response: str = handle_response(new_text)
#         else:
#             return
#     else:
#         response: str = handle_response(text)
#
#     print('Bot:', response)
#     await update.message.reply_text(response)
#
# async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print(f'Update {update} caused error {context.error}')
#
# if __name__ == '__main__':
#     print('Starting bot...')
#     app = Application.builder().token(TOKEN).read_timeout(30).build()
#
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('generatev2ray', generatev2ray_command)],
#         states={
#             SELECT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_name)],
#             GET_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_id)]
#         },
#         fallbacks=[],
#     )
#
#     app.add_handler(conv_handler)
#     app.add_handler(CommandHandler('start', start_command))
#     app.add_handler(CommandHandler('custom', custom_command))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
#     app.add_error_handler(error)
#
#     print('Polling...')
#     app.run_polling(poll_interval=3)

import commands.commands as commands

from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, \
    MessageHandler, CallbackContext, Updater, filters

application = Application.builder().token('6861190199:AAGwpAT3dBRaXAgZDV-MpkxIEMCfUGkBsQg').build()

application.add_handler(CommandHandler("start", commands.start))
application.add_handler(CommandHandler('language', commands.language))
application.add_handler(CommandHandler("help", commands.help))
application.add_handler(CommandHandler('setDotaId', commands.setDotaId))
application.add_handler(CommandHandler('getInfo', commands.getInfo))
application.add_handler(CommandHandler('setPriorityRole', commands.setPriorityRole))
import configparser

from messages.messages import message, setLanguage, current_language

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, \
    MessageHandler, CallbackContext, Updater, filters

start_message = 'start.message'
help_message = 'help.message'
language_no_argument_exception = 'language.noArgumentException'
language_no_correct_exception = 'language.noCorrectException'
language_warning = 'language.warning'
language_set = 'language.set'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(message(start_message, 'start', update.effective_user.first_name))


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(message(start_message, 'start', update.effective_user.first_name))


async def language(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        await update.message.reply_text(message(language_no_argument_exception, 'language'))

    value = str(context.args[0])
    try:
        if value == current_language:
            await update.message.reply_text(message(language_warning, 'language', value))
        else:
            setLanguage(value)

        await update.message.reply_text(message(language_set, 'language', value))
    except ValueError:
        await update.message.reply_text(message(language_no_correct_exception, 'language'))

import requests

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
dotaId_no_argument_exception = 'dotaId.noArgumentException'
dotaId_no_correct_exception = 'dotaId.noCorrectException'
dotaId_not_found_exception = 'dotaId.noFoundException'
dotaId_warning = 'dotaId.warning'
dotaId_set = 'dotaId.set'
dotaId_help = 'dotaId.help'

users = {

}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(message(start_message, 'start', update.effective_user.first_name))


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(message(help_message, 'help', update.effective_user.first_name))


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


async def setDotaId(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    try:
        if context.args[0] == 'help':
            await update.message.reply_text(message(dotaId_help, 'dotaId'))
            return

        if not context.args[0].isdigit():
            await update.message.reply_text(message(dotaId_no_correct_exception, 'dotaId'))
            return

        player_id = context.args[0]
        url = f'https://api.opendota.com/api/players/{player_id}'
        response = requests.get(url)

        if response.status_code == 200:
            if not (user_id in users):
                users[user_id] = {'dotaId': int(player_id)}
                await update.message.reply_text(message(dotaId_set, 'dotaId', player_id))
            else:
                await update.message.reply_text(message(dotaId_warning, 'dotaId'))
        else:
            await update.message.reply_text(message(dotaId_not_found_exception, 'dotaId', player_id))
    except IndexError:
        await update.message.reply_text(message(dotaId_no_argument_exception, 'dotaId'))
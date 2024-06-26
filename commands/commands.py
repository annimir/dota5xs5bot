import requests

from commands.methods import getRank, getMmr, getRatingFromPosition, isAllNumbersInRoles, convertStrRoletToIntRole
from messages.messages import message, default_language

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
getInfo_not_found_exception = 'getInfo.notFoundException'
getInfo_message = 'getInfo.message'
setRoles_no_argument_exception='setRoles.noArgumentException'
setRoles_not_found_Exception='setRoles.notFoundException'
setRoles_no_correct_Exception='setRoles.noCorrectException'
setRoles_set='setRoles.set'
setRoles_help='setRoles.help'

users = {}
users_language = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if not (user_id in users_language):
        users_language[user_id] = default_language
    await update.message.reply_text(message(users_language[user_id], start_message, 'start', update.effective_user.first_name))


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    await update.message.reply_text(message(users_language[user_id], help_message, 'help', update.effective_user.first_name))


async def language(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if len(context.args) != 1:
        await update.message.reply_text(message(users_language[user_id], language_no_argument_exception, 'language'))

    value = str(context.args[0])
    try:
        if value == users_language[user_id]:
            await update.message.reply_text(message(users_language[user_id], language_warning, 'language', value))
        else:
            users_language[user_id] = value

        await update.message.reply_text(message(users_language[user_id], language_set, 'language', value))
    except ValueError:
        await update.message.reply_text(message(users_language[user_id], language_no_correct_exception, 'language'))


async def setDotaId(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    try:
        if context.args[0] == 'help':
            await update.message.reply_text(message(users_language[user_id], dotaId_help, 'dotaId'))
            return

        if not context.args[0].isdigit():
            await update.message.reply_text(message(users_language[user_id],  dotaId_no_correct_exception, 'dotaId'))
            return

        player_id = context.args[0]
        url = f'https://api.opendota.com/api/players/{player_id}'
        response = requests.get(url)

        if response.status_code == 200:
            if not (user_id in users):
                data = response.json()
                rank_tier = int(data['rank_tier'])
                leaderboard_rank = int(data['leaderboard_rank']) if data['leaderboard_rank'] is not None else 0
                mmr = getMmr(rank_tier) if rank_tier < 80 else getRatingFromPosition(leaderboard_rank)
                users[user_id] = {
                    'account_id': int(player_id),
                    'name': data['profile']['personaname'],
                    'avatar': data['profile']['avatarmedium'],
                    'rank': getRank(users_language[user_id], rank_tier, leaderboard_rank),
                    'mmr': mmr,
                    'positions': []
                }
                await update.message.reply_text(message(users_language[user_id], dotaId_set, 'dotaId', player_id))
            else:
                await update.message.reply_text(message(users_language[user_id], dotaId_warning, 'dotaId'))
        else:
            await update.message.reply_text(message(users_language[user_id], dotaId_not_found_exception, 'dotaId', player_id))
    except IndexError:
        await update.message.reply_text(message(users_language[user_id], dotaId_no_argument_exception, 'dotaId'))


async def getInfo(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    if user_id in users:
        user = users[user_id]
        await context.bot.send_photo(chat_id=chat_id,
                                     photo=user['avatar'],
                                     caption=message(users_language[user_id],
                                                     getInfo_message, 'getInfo',
                                                     user['name'], user['rank'],
                                                     user['mmr'], user['positions']))
    else:
        await update.message.reply_text(users_language[user_id], message(dotaId_not_found_exception, 'getInfo', user_id))


async def setPriorityRole(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in users:
        try:
            if context.args[0] == 'help':
                await update.message.reply_text(message(users_language[user_id], setRoles_help, 'setRoles'))
                return

            args = convertStrRoletToIntRole(context.args)
            if not isAllNumbersInRoles(args):
                await update.message.reply_text(message(users_language[user_id], setRoles_no_correct_Exception, 'setRoles'))
                return

            positions = ', '.join(map(str, args))
            users[user_id]['positions'] = positions
            await update.message.reply_text(message(users_language[user_id], setRoles_set, 'setRoles', positions))
        except IndexError:
            await update.message.reply_text(message(users_language[user_id], setRoles_no_argument_exception, 'setRoles'))

    else:
        await update.message.reply_text(message(users_language[user_id], setRoles_not_found_Exception, 'setRoles', user_id))


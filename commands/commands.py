import asyncio
import requests

from commands.methods import getRank, getMmr, getRatingFromPosition, isAllNumbersInRoles, convertStrRoletToIntRole, \
    balance_teams
from messages.messagePath import start_message, help_message, language_no_argument_exception, language_warning, \
    language_set, language_no_correct_exception, dotaId_help, dotaId_no_correct_exception, dotaId_set, dotaId_warning, \
    dotaId_not_found_exception, dotaId_no_argument_exception, getInfo_message, setRoles_not_found_Exception, \
    setRoles_help, setRoles_no_correct_Exception, setRoles_set, setRoles_no_argument_exception, createMatch_timeout, \
    createMatch_no_found_exception, createMatch_warning, createMatch_create, createMatch_send_Notification, \
    accept_no_createMatch_exception, accept_no_found_exception, accept_warning, accept_message, \
    accept_send_notification, createMatch_start, decline_message, decline_no_accept_exception, \
    decline_no_found_exception, decline_no_createMatch_exception, gameInfo_player, gameInfo_team
from messages.messages import message, default_language

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, \
    MessageHandler, CallbackContext, Updater, filters

users = {}
users_language = {}
user_chat_ids = set()

match_state = {
    "isCreate": False,
    "author": None,
    "accepted_users": dict(),
    "task": None
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    user_chat_ids.add(chat_id)
    if not (chat_id in users_language):
        users_language[chat_id] = default_language
    await update.message.reply_text(
        message(users_language[chat_id], start_message, 'start', update.effective_user.first_name))


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text(
        message(users_language[chat_id], help_message, 'help', update.effective_user.first_name))


async def language(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    if len(context.args) != 1:
        await update.message.reply_text(message(users_language[chat_id], language_no_argument_exception, 'language'))
        return

    value = str(context.args[0])
    try:
        if value == users_language[chat_id]:
            await update.message.reply_text(message(users_language[chat_id], language_warning, 'language', value))
            return

        users_language[chat_id] = value
        await update.message.reply_text(message(users_language[chat_id], language_set, 'language', value))
    except ValueError:
        await update.message.reply_text(message(users_language[chat_id], language_no_correct_exception, 'language'))


async def setDotaId(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    try:
        if context.args[0] == 'help':
            await update.message.reply_text(message(users_language[chat_id], dotaId_help, 'dotaId'))
            return

        if not context.args[0].isdigit():
            await update.message.reply_text(message(users_language[chat_id], dotaId_no_correct_exception, 'dotaId'))
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
                    'rank': getRank(users_language[chat_id], rank_tier, leaderboard_rank),
                    'mmr': mmr,
                    'positions': []
                }
                await update.message.reply_text(message(users_language[chat_id], dotaId_set, 'dotaId', player_id))
            else:
                await update.message.reply_text(message(users_language[chat_id], dotaId_warning, 'dotaId'))
        else:
            await update.message.reply_text(
                message(users_language[chat_id], dotaId_not_found_exception, 'dotaId', player_id))
    except IndexError:
        await update.message.reply_text(message(users_language[chat_id], dotaId_no_argument_exception, 'dotaId'))


async def getInfo(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    if not (user_id in users):
        await update.message.reply_text(users_language[chat_id],
                                        message(dotaId_not_found_exception, 'getInfo', user_id))
        return

    user = users[user_id]
    await context.bot.send_photo(chat_id=chat_id, photo=user['avatar'],
                                 caption=message(users_language[user_id], getInfo_message, 'getInfo',
                                                 user['name'], user['rank'], user['mmr'], user['positions']))


async def setPriorityRole(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    if not (user_id in users):
        await update.message.reply_text(message(users_language[chat_id], setRoles_not_found_Exception, 'setRoles'))
        return

    try:
        if context.args[0] == 'help':
            await update.message.reply_text(message(users_language[chat_id], setRoles_help, 'setRoles'))
            return

        args = convertStrRoletToIntRole(context.args)
        if not isAllNumbersInRoles(args):
            await update.message.reply_text(
                message(users_language[chat_id], setRoles_no_correct_Exception, 'setRoles'))
            return

        positions = ', '.join(map(str, args))
        users[user_id]['positions'] = positions
        await update.message.reply_text(message(users_language[chat_id], setRoles_set, 'setRoles', positions))

    except IndexError:
        await update.message.reply_text(
            message(users_language[chat_id], setRoles_no_argument_exception, 'setRoles'))


async def match_timeout(context: CallbackContext):
    if len(match_state["accepted_users"]) < 10:
        for chat_id in user_chat_ids:
            await context.bot.send_message(
                chat_id=chat_id, text=message(users_language[chat_id], createMatch_timeout, 'createMatch'))
        match_state["isCreate"] = False
        match_state["accepted_users"] = dict()
        match_state['author'] = None


async def createMatch(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    if not (user_id in users):
        await update.message.reply_text(
            message(users_language[chat_id], createMatch_no_found_exception, 'createMatch'))
        return

    if match_state['isCreate']:
        await update.message.reply_text(
            message(users_language[chat_id], createMatch_warning, 'createMatch', match_state['author']))
        return

    match_state['author'] = users[user_id]['name']
    match_state['isCreate'] = True
    match_state['accepted_users'][user_id] = users[user_id]

    await update.message.reply_text(message(users_language[chat_id], createMatch_create, 'createMatch', 15))
    for user_chat_id in user_chat_ids:
        if user_chat_id != chat_id:
            await context.bot.send_message(
                chat_id=user_chat_id, text=message(
                    users_language[user_chat_id], createMatch_send_Notification, 'createMatch'))

    match_state["task"] = context.application.create_task(asyncio.sleep(900))
    match_state["task"].add_done_callback(lambda _: asyncio.create_task(match_timeout(context)))


async def accept(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    if not match_state['isCreate']:
        await update.message.reply_text(message(users_language[chat_id], accept_no_createMatch_exception, 'accept'))
        return

    if not (user_id in users):
        await update.message.reply_text(message(users_language[chat_id], accept_no_found_exception, 'accept'))
        return

    if user_id in match_state['accepted_users']:
        await update.message.reply_text(message(users_language[chat_id], accept_warning, 'accept'))
        return

    match_state['accepted_users'][user_id] = users[user_id]
    await update.message.reply_text(
        message(users_language[chat_id], accept_message, 'accept',
                match_state['author'], len(match_state['accepted_users'])))

    for user_chat_id in user_chat_ids:
        if user_chat_id != chat_id:
            await context.bot.send_message(chat_id=user_chat_id, text=message(
                users_language[user_chat_id], accept_send_notification, 'accept', users[user_id]['name'],
                len(match_state['accepted_users'])))

    if len(match_state['accepted_users']) == 10:

        # Здесь необходимо добавить расперделение по двум командам так,
        # чтобы средний рейтинг каждой был сбалансированный, а также учитывал приоритетные позиции
        team1, team2 = balance_teams(list(match_state["accepted_users"].values()))

        for user_chat_id in user_chat_ids:
            await context.bot.send_message(chat_id=user_chat_id, text=message(
                users_language[user_chat_id], createMatch_start, 'createMatch'))

        await notify_teams(context, team1, team2)

        match_state["task"].cancel()
        match_state['author'] = None
        match_state["match_created"] = False
        match_state["accepted_users"] = dict()


async def notify_teams(context, team1, team2):
    for user_chat_id in user_chat_ids:
        team1_str = "\n".join(
            [message(users_language[user_chat_id], gameInfo_player, 'gameInfo', user['name'], user['positions'],
                     user['mmr']) for user in team1])
        team2_str = "\n".join(
            [message(users_language[user_chat_id], gameInfo_player, "gameInfo", user['name'], user['positions'],
                     user['mmr']) for user in team2])

        text = message(users_language[user_chat_id], gameInfo_team, 'gameInfo', team1_str, team2_str,
                       match_state['author'])

        await context.bot.send_message(chat_id=user_chat_id, text=text)


async def decline(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    if not match_state['isCreate']:
        await update.message.reply_text(message(users_language[chat_id], decline_no_createMatch_exception, 'decline'))
        return

    if not (user_id in users):
        await update.message.reply_text(message(users_language[chat_id], decline_no_found_exception, 'decline'))
        return

    if not (users[user_id] in match_state['accepted_users']):
        await update.message.reply_text(message(users_language[chat_id], decline_no_accept_exception, 'decline'))
        return

    decline_user = match_state['accepted_users'].pop(user_id)
    await update.message.reply_text(
        message(users_language[chat_id], decline_message, 'decline',
                match_state['author'], len(match_state['accepted_users'])))

    for user_chat_id in user_chat_ids:
        if user_chat_id != chat_id:
            await context.bot.send_message(chat_id=user_chat_id, text=message(
                users_language[user_chat_id], accept_send_notification, 'decline', decline_user['name'],
                len(match_state['accepted_users'])))

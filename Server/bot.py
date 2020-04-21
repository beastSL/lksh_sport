import config as cfg
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, parsemode
from json import dump, load
import requests

token = cfg.tg_token
request_kwargs = {
    'proxy_url': cfg.proxy_url,
    # Optional, if you need authentication:
    # 'urllib3_proxy_kwargs': {
    #    'username': cfg.proxy_user,
    #    'password': cfg.proxy_pass,
    # }
}
updater = Updater(
    token=cfg.tg_token,
    request_kwargs=request_kwargs,
    use_context=True
)
dispatcher = updater.dispatcher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def logMessage(message):
    logging.log(
        logging.INFO,
        f'{message.chat.username} sent a message: \"{message.text}\"'
    )


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="The bot is ready" if update.message.chat.username in cfg.admins
        else cfg.sorry
    )
    logMessage(update.message)


def stop(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="The bot is stopped" if update.message.chat.username in cfg.admins
        else cfg.sorry
    )
    logMessage(update.message)
    if update.message.chat.username in cfg.admins:
        updater.stop()
        requests.post(
            'http://127.0.0.1:42069/api/admin/shutdown',
            data={'token': 'denislox'}
        )


def requestApproval(args):
    sirgay_id = cfg.sirgay_id
    reply_markup = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                'Подтвердить',
                callback_data=f'1 {args["hash"]}'
            ),
            InlineKeyboardButton(
                'Отклонить',
                callback_data=f'0 {args["hash"]}'
            )
        ]]
    )
    text = f'Поступила новая заявка на регистрацию\n№{args["hash"]}\n'
    if args['no-team'] is not None:
        text += f'Одиночный участник\n'
        text += f'Имя, фамилия: {args["participant"]}\n'
        text += f'Спорт: {args["sport"]}'
        updater.bot.send_message(
            chat_id=sirgay_id,
            text=text,
            reply_markup=reply_markup
        )
    else:
        text += f'Название команды: {args["team-name"]}\n'
        i = 1
        while args.get(f'participant-{i}', '') != '':
            text += f'Участник {i}: {args[f"participant-{i}"]}\n'
            i += 1
        text += f'Спорт: {args["sport"]}'
        updater.bot.send_message(
            chat_id=sirgay_id,
            text=text,
            reply_markup=reply_markup
        )


def button(update, context):
    query = update.callback_query
    result, args_hash = query.data.split()
    if result == '1':
        approveRegistration(args_hash)
    else:
        denyRegistration(args_hash)


def approveRegistration(args_hash):
    response = requests.post(
        'http://127.0.0.1:42069/api/admin/approve_registration',
        data={'token': args_hash}
    )


def denyRegistration(args_hash):
    response = requests.post(
        'http://127.0.0.1:42069/api/admin/deny_registration',
        data={'token': args_hash}
    )


def success(args_hash, result):
    sirgay_id = cfg.sirgay_id
    updater.bot.send_message(
        chat_id=sirgay_id,
        text=f'Заявка с кодовым номером\n№{args_hash}\nбыла успешно {result}'
    )


start_handler = CommandHandler('start', start)
stop_handler = CommandHandler('stop', stop)
approve_handler = CallbackQueryHandler(button)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(approve_handler)


def init():
    updater.start_polling()

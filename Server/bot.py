import config as cfg
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

token = cfg.tg_token
request_kwargs = {
    # 'proxy_url': cfg.proxy_url,
    # # Optional, if you need authentication:
    # 'urllib3_proxy_kwargs': {
    #     'username': cfg.proxy_user,
    #     'password': cfg.proxy_pass,
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


def approve_registration(args):
    sirgay_id = '228546319'
    updater.bot.send_message(
        chat_id=sirgay_id,
        text='Поступило новое заявление на регистрацию!\n'
    )
    print(args['no-team'] is not None)
    if args['no-team'] is not None:
        updater.bot.send_message(
            chat_id=sirgay_id,
            text=f'Одиночный участник\n'
            f'Имя, фамилия: {args["participant"]}\n'
            f'Спорт: {args["sport"]}'
        )
    else:
        text = f'Название команды: {args["team-name"]}\n'
        i = 1
        while args.get(f'participant-{i}', '') != '':
            text += f'Участник {i}: {args[f"participant-{i}"]}\n'
            i += 1
        text += f'Спорт: {args["sport"]}'
        updater.bot.send_message(
            chat_id=sirgay_id,
            text=text
        )


def init():
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()

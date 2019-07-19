import config as cfg
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

token = cfg.tg_token
request_kwargs = {
    'proxy_url': cfg.proxy_url,
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'username': cfg.proxy_user,
        'password': cfg.proxy_pass,
    }
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
        text="You are a faggot"
    )
    logMessage(update.message)


def echo(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="@beast_sl is a faggot"
    )
    logMessage(update.message)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
updater.idle()

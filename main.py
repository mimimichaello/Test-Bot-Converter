# t.me/CashConvertProBot

from telegram.ext import Updater, Filters, MessageHandler
from telegram.ext import CommandHandler

from handlers import (
    start,
    help,
    convert,
    handle_text_message,
    goodbye,
    perform_conversion,
)
from config import BOT_TOKEN


updater = Updater(BOT_TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler("convert", convert))
updater.dispatcher.add_handler(
    MessageHandler(
        Filters.text & Filters.regex(r"^\d+\s\w{3}\sto\s\w{3}$"), perform_conversion
    )
)
updater.dispatcher.add_handler(
    MessageHandler(
        Filters.text & ~Filters.command & ~Filters.regex(r"^\d+\s\w{3}\sto\s\w{3}$"),
        handle_text_message,
    )
)
updater.dispatcher.add_handler(
    MessageHandler(Filters.status_update.left_chat_member, goodbye)
)

updater.start_polling()

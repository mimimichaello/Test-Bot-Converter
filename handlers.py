import requests
import logging

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext

from config import API_KEY, API_URL

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    logger.info(f"User {update.message.from_user.username} started the bot")
    update.message.reply_text(
        "Привет! Я бот конвертации валют. Используй /help для получения списка доступных команд."
    )


def help(update: Update, context: CallbackContext) -> None:
    logger.info(f"User {update.message.from_user.username} asked for help")
    update.message.reply_text(
        "Список доступных команд:\n\n/convert - конвертировать валюту(для конвертации введите команду /convert или нажмите на кнопку Конвертация\n/help - получить список доступных команд"
    )


def goodbye(update: Update, context: CallbackContext) -> None:
    logger.info(f"User {update.message.from_user.username} left the chat")
    update.message.reply_text("До свидания!")


def handle_text_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text.lower()
    if any(word in text for word in ["привет", "здравствуй", "добрый день"]):
        update.message.reply_text("Привет!")
    elif any(word in text for word in ["пока", "до свидания", "досвидания"]):
        update.message.reply_text("До свидания!")
    else:
        update.message.reply_text("Извините, я не понимаю ваш запрос.")


def convert(update: Update, context: CallbackContext) -> None:
    logger.info(f"User {update.message.from_user.username} asked for conversion")
    update.message.reply_text(
        "Введите сумму, исходную валюту и целевую валюту в формате: <сумма> <исходная валюта> to <целевая валюта>. Пример: 100 USD to EUR"
    )


def perform_conversion(update: Update, context: CallbackContext) -> None:
    logger.info(f"User {update.message.from_user.username} asked for conversion")
    api_key = API_KEY
    api_url = API_URL

    text = update.message.text
    parts = text.split()
    if len(parts) == 4 and parts[2].lower() == "to":
        amount = parts[0]
        base_currency = parts[1].upper()
        target_currency = parts[3].upper()
        response = requests.get(f"{api_url}/{base_currency}?api_key={api_key}")
        data = response.json()
        if "rates" in data and target_currency in data["rates"]:
            conversion_rate = data["rates"][target_currency]
            result = float(amount) * conversion_rate
            update.message.reply_text(
                f"{amount} {base_currency} равно {result} {target_currency}"
            )
        else:
            update.message.reply_text(
                "К сожалению, не удалось найти обменный курс для указанных валют."
            )
    else:
        update.message.reply_text(
            "Пожалуйста, введите данные в правильном формате: <сумма> <исходная валюта> to <целевая валюта>. Пример: 100 USD to EUR"
        )

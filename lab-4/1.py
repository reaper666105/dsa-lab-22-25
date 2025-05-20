"""
Автор: Юшков Вадим, ФБИ-22
Лабораторная работа №4: Бот для работы с валютами
"""

import telebot
import os
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения курсов валют
currency_rates = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "Здравствуйте! Это персональный бот для выполнения лабораторной работы №4.\n"
        "Вы можете сохранять и конвертировать курсы валют.\n"
        "Команда /save_currency — задать курс новой валюты.\n"
        "Команда /convert — сконвертировать валюту в рубли."
    )

@bot.message_handler(commands=['save_currency'])
def save_currency(message):
    msg = bot.reply_to(message, "Пожалуйста, укажите код валюты (например, USD, EUR):")
    bot.register_next_step_handler(msg, save_currency_name)

def save_currency_name(message):
    currency_name = message.text.strip().upper()
    msg = bot.reply_to(message, f"Пожалуйста, введите курс {currency_name} к рублю (например, 85.5):")
    bot.register_next_step_handler(msg, save_currency_rate, currency_name)

def save_currency_rate(message, currency_name):
    try:
        rate = float(message.text.replace(',', '.'))
        currency_rates[currency_name] = rate
        bot.reply_to(message, f"Курс {currency_name} успешно сохранён: {rate} руб.")
    except ValueError:
        bot.reply_to(message, "Ошибка! Введите корректное числовое значение курса (например, 85.5).")

@bot.message_handler(commands=['convert'])
def convert(message):
    msg = bot.reply_to(message, "Введите название валюты (например, USD, EUR):")
    bot.register_next_step_handler(msg, convert_currency_name)

def convert_currency_name(message):
    currency_name = message.text.strip().upper()
    if currency_name not in currency_rates:
        bot.reply_to(
            message,
            f"Курс для валюты {currency_name} не найден. Используйте /save_currency для добавления новой валюты."
        )
        return
    msg = bot.reply_to(message, f"Пожалуйста, введите сумму в {currency_name} для конвертации:")
    bot.register_next_step_handler(msg, convert_amount, currency_name)


def convert_amount(message, currency_name):
    try:
        amount = float(message.text.replace(',', '.'))
        rate = currency_rates[currency_name]
        result = amount * rate
        bot.reply_to(
            message,
            f"{amount} {currency_name} = {round(result, 2)} руб. (по курсу {rate})"
        )
    except ValueError:
        bot.reply_to(message, "Ошибка! Введите корректное числовое значение суммы (например, 100).")

if __name__ == '__main__':
    print("Бот для лабораторной работы запущен...")
    bot.polling()
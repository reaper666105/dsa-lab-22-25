import telebot
API_TOKEN = '7893977094:AAGbnPf0RzQsx6LmtyLNsMcVqs7zLiH3klA'
bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения курсов валют
currency_rates = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "Привет! Я бот для работы с валютами.\n"
        "Используй /save_currency чтобы сохранить курс валюты\n"
        "Используй /convert чтобы конвертировать валюту в рубли"
    )

@bot.message_handler(commands=['save_currency'])
def save_currency(message):
    msg = bot.reply_to(message, "Введите название валюты (например, USD, EUR):")
    bot.register_next_step_handler(msg, save_currency_name)

def save_currency_name(message):
    currency_name = message.text.upper()
    msg = bot.reply_to(message, f"Введите курс {currency_name} к рублю (например, 75.5):")
    bot.register_next_step_handler(msg, save_currency_rate, currency_name)

def save_currency_rate(message, currency_name):
    try:
        rate = float(message.text.replace(',', '.'))
        currency_rates[currency_name] = rate
        bot.reply_to(message, f"Курс {currency_name} сохранён: {rate} руб.")
    except ValueError:
        bot.reply_to(message, "Ошибка! Введите число (например, 75.5).")

@bot.message_handler(commands=['convert'])
def convert(message):
    msg = bot.reply_to(message, "Введите название валюты (например, USD, EUR):")
    bot.register_next_step_handler(msg, convert_currency_name)

def convert_currency_name(message):
    currency_name = message.text.upper()
    if currency_name not in currency_rates:
        bot.reply_to(message, f"Курс для {currency_name} не найден. Попробуйте /save_currency.")
        return
    
    msg = bot.reply_to(message, f"Введите сумму в {currency_name} для конвертации:")
    bot.register_next_step_handler(msg, convert_amount, currency_name)

def convert_amount(message, currency_name):
    try:
        amount = float(message.text.replace(',', '.'))
        rate = currency_rates[currency_name]
        result = amount * rate
        bot.reply_to(message, f"{amount} {currency_name} = {round(result, 2)} руб. (курс: {rate})")
    except ValueError:
        bot.reply_to(message, "Ошибка! Введите число (например, 100).")

if __name__ == '__main__':
    print("Бот запущен...")

import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConvertor

bot = telebot.TeleBot(TOKEN)

@bot.message_handler (commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в сследующем формате: \
\n<имя валюты> <в какую валюту переввести> <количество переводимой валюты>\
\n Внимание: !!!Все данные вводить строчными буквами!!!\
\n Чтобы увидеть список валют, введите команду /values'
    bot.reply_to(message, text)

@bot.message_handler (commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message:telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Параметры введены не верно')

        quote, base, amount = values
        total_base = CryptoConvertor.get_price(quote, base, amount)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()
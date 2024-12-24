import telebot
from telebot import apihelper
import requests
import json

apihelper.proxy = {'https': 'socks5://127.0.0.1:64238'}

bot = telebot.TeleBot('7956634680:AAEYrGIEZlz3QNv3xh_4538H-1b-l9IXrc4')
API = '8aedde1c64b15e0d5df8ebec742a04b4'

proxies = {
    'https': 'socks5://127.0.0.1:64238'  # HTTPS-прокси из логов Psiphon
}

# Запуск вывод сообщения
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Приветствую, рад вас видеть! Напишите название города в котором хотели бы узнать погоду')

# Ответ на текст пользователя
@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&lang=ru&units=metric', proxies=proxies)
    # Обрабатываем ошибки если пользователь ввел неверные данные
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        main = data["weather"][0]["main"]
        description = data["weather"][0]["description"]
        bot.reply_to(message, f'''Сейчас погода:  {temp}°C
Ощущается:  {data["main"]['feels_like']}°C
{str(description).capitalize()}''')
        # Отправляем еще изображение в ответе пользователю
        # image = 'sunny.jpg' if temp > 5.0 else 'winter.jpg'
        if main == 'Clouds':
            file = open(f'Telegram Bots/weather bot/cloudly.jpg', 'rb')
        elif main == 'Snow':
            file = open(f'Telegram Bots/weather bot/snow.jpg', 'rb')
        elif main == 'Rain':
            file = open(f'Telegram Bots/weather bot/rain.jpg', 'rb')
        elif temp > 5.0 and main == 'Clear':
            file = open(f'Telegram Bots/weather bot/sunny.jpg', 'rb')
        else:
            file = open(f'Telegram Bots/weather bot/winter.jpg', 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, f'Город указан не верно')

bot.polling(none_stop=True)




# Сейчас погода: {
#              'coord': {
#                'lon': 27.5667,
#                'lat': 53.9},
#             'weather': [{
#               'id': 804,
#               'main': 'Clouds',
#               'description': 'overcast clouds', 
#               'icon': '04d'}], 
#             'base': 'stations',
#             'main': {
#               'temp': 6.11,
#               'feels_like': 0.31,
#               'temp_min': 6.11,
#               'temp_max': 6.11,
#               'pressure': 993,
#               'humidity': 72,
#               'sea_level': 993,
#               'grnd_level': 966}, 
#             'visibility': 10000,
#             'wind': {
#               'speed': 13.35,
#               'deg': 291, 
#               'gust': 22.6}, 
#             'clouds': {'all': 89}, 
#             'dt': 1734345972, 
#             'sys': {
#               'country': 'BY',
#               'sunrise': 1734330182,
#               'sunset': 1734356881}, 
#             'timezone': 10800, 'id': 625144, 'name': 'Minsk', 'cod': 200}
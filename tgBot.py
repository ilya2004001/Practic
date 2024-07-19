import pyowm
import telebot
from pyowm.utils.config import get_default_config
from pyowm.commons.exceptions import NotFoundError

# Установите API ключи
owm = pyowm.OWM('a68c3f780bb8d0c4f861a73f10e70ef0')
bot = telebot.TeleBot("7014379328:AAF9vcLnmnMw1pNk4OSsmnzl00QbGQedE6M", parse_mode=None)

# Укажите язык (опционально, здесь указано на русском)
config_dict = get_default_config()
config_dict['language'] = 'ru'

# Получите менеджер для работы с погодой
mgr = owm.weather_manager()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который поможет узнать погоду. ")
    bot.send_message(message.chat.id, "Пожалуйста, напиши название города, чтобы узнать текущую погоду.")

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def send_echo(message):
    try:
        observation = mgr.weather_at_place(message.text)
        w = observation.weather
        temp = w.temperature('celsius')['temp']
        wind_speed = w.wind()['speed']
        status = w.detailed_status
        clouds = w.clouds
        rain = w.rain
        snow = w.snow

        answer = f"Температура в {message.text}: {temp}°C\n"
        answer += f"Порыв ветра: {wind_speed} м/с\n"
        answer += f"Облачность: {clouds}%\n"
        answer += f"Статус: {status}\n"

        if temp > 25:
            answer += "На улице жарко, надевайте легкую одежду и не забудьте солнцезащитные очки."
        elif 15 <= temp <= 25:
            answer += "На улице тепло, подойдет легкая одежда, возможно, кофточка или легкая куртка."
        elif 5 <= temp < 15:
            answer += "На улице прохладно, надевайте куртку и что-нибудь теплое."
        else:
            answer += "На улице холодно, обязательно надевайте теплую одежду, шапку и перчатки."

        if wind_speed > 10:
            answer += " Также учтите, что сильный ветер, может понадобиться ветровка или шарф."

        if rain:
            answer += " Похоже, будет дождь, возьмите зонт или дождевик."
        if snow:
            answer += " Ожидается снег, оденьтесь потеплее и возьмите зимнюю обувь."

        bot.send_message(message.chat.id, answer)
    except NotFoundError:
        bot.send_message(message.chat.id, "Такого города не существует.")

bot.polling(non_stop=True)

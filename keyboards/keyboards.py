from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
btn_rates = KeyboardButton('Курсы валют 💰')
btn_weather = KeyboardButton('Погода 🌞')
kb_main_menu.add(btn_rates, btn_weather)

# Keyboards - Rates
kb_rates_when = ReplyKeyboardMarkup(resize_keyboard=True)
btn_rates_on_today = KeyboardButton('На сегодня 📅')
btn_rates_on_date = KeyboardButton('На дату 📅')
kb_rates_when.add(btn_rates_on_today, btn_rates_on_date)

# Keyboards - Weather
kb_weather_where = ReplyKeyboardMarkup(resize_keyboard=True)
btn_weather_brest = KeyboardButton('Брест')
btn_weather_vitebsk = KeyboardButton('Витебск')
btn_weather_gomel = KeyboardButton('Гомель')
btn_weather_grodno = KeyboardButton('Гродно')
btn_weather_minsk = KeyboardButton('Минск')
btn_weather_mogilev = KeyboardButton('Могилев')
kb_weather_where.add(btn_weather_brest, btn_weather_vitebsk, btn_weather_gomel,
                     btn_weather_grodno, btn_weather_minsk, btn_weather_mogilev)

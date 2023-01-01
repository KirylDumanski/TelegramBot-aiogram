# WeatherCurrencyTGBot

## Introduction
This is a telegram bot written in Python using the aiogram asynchronous framework for 
Telegram Bot API.

It provides the following options:
- Сurrent weather - you can find out the current weather in the cities from 
the proposed list. In this case there has been used simple and fast and free
weather API from [OpenWeatherMap](https://openweathermap.org/api)

- Exchange rates - you can find out the actual exchange rates for today or a specific date.
This functionality is supported by using the 
[API of the National Bank of the Republic of Belarus](https://www.nbrb.by/apihelp/exrates)

## Ger your own credentials

### Obtain Your Telegram Bot Token
In this context, a token is a string that authenticates your bot (not your account) on the bot API.
Each bot has a unique token which can also be revoked at any time via [@BotFather](https://t.me/botfather).

Obtaining a token is as simple as contacting [@BotFather](https://t.me/botfather), issuing the `/newbot` command
and following the steps until you're given a new token. You can find a step-by-step guide
[here](https://core.telegram.org/bots/features#creating-a-new-bot).

Your token will look something like this:
```
4839574812:AAFD39kkdpWt3ywyRZergyOLMaJhac60qc
```

### Get Your OpenWeatherMap API Key:
The API key is all you need to call any of our weather APIs. Once you [sign up](https://openweathermap.org/home/sign_up)
using your email, the API key (APPID) will be sent to you in a confirmation email. Your API keys can always be found 
on your [account page](https://home.openweathermap.org/api_keys), where you can also generate additional API keys if needed. 
Check our [documentation page](https://openweathermap.org/api) to find all technical information for each product. 
Documentation is an essential guide with actual examples and comprehensive description of API calls, responses and parameters.

### Get your Telegram ID
1. Follow the link [@getmyid_bot](https://t.me/getmyid_bot)
2. Click on the "Start" button to start the bot.
3. Your ID will be displayed immediately in the reply message. See the first line, which starts with "Your user". 


## Installation and run guide
1. Clone git repository:
```
https://github.com/KirylDumanski/WeatherCurrencyTGBot.git
```
2. Execute in terminal:
```
python pip install -r requirements.txt
```
3. In `data` folder find and rename `.env.dist` to `.env`. Paste your credentials into it:
```
BOT_TOKEN=123456789:YouR_Bot_TokEn
WEATHER_TOKEN=Your_openweather_api_token
ADMIN=YOUR_TG_ID
```
4. Execute in terminal to run app:
```
python app.py
```







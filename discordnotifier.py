from telebot import TeleBot
from json import loads
from loguru import logger
from sys import stderr
from msvcrt import getch
from ctypes import windll
from os import system
import requests


def take_chat_id():
	r = requests.get(f'https://api.telegram.org/bot{tgbot_key}/getUpdates?offset=-1')
	chat_id = r.json()['result'][0]['message']['chat']['id']
	nickname = r.json()['result'][0]['message']['chat']['first_name']
	check_posts(None, chat_id, nickname)


def check_posts(old_msg_id, chat_id, nickname):
	logger.success(f'The bot has been successfully launched, waiting for new posts\ntg acc is {nickname}')
	while True:
		try:
			r = requests.get(f'https://discord.com/api/v9/channels/{ds_chatid}/messages?limit=1', headers={'authorization': ds_token})
			new_msg_id = loads(r.text)[0]['id']
			if old_msg_id == None or int(old_msg_id) != int(new_msg_id):
				msg_text = loads(r.text)[0]['content']
				if old_msg_id != None:
					if len(msg_text) > 0:
						requests.post(f'https://api.telegram.org/bot{tgbot_key}/sendMessage',
									  json={'chat_id': chat_id, 'text': f'New post:\n{str(msg_text)}'})

					else:
						requests.post(f'https://api.telegram.org/bot{tgbot_key}/sendMessage',
									  json={'chat_id': chat_id, 'text': 'New post: empty'})
					logger.success('A new post. The information was successfully sent to Telegram')
				old_msg_id = new_msg_id
		except:
			pass


windll.kernel32.SetConsoleTitleW('Discord Notifier')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")

tgbot_key = str(input('botkey from tg @botfather: '))
ds_token = str(input('dstoken from f12: '))
ds_chatid = int(input('ds chatid from link: '))
bot = TeleBot(tgbot_key)

take_chat_id()


import common

import os
import sys

import json
import bot



def main():

	print("Booting")

	common.init()

	telegram_bot_token=""


	# READ API TOKENS FROM FILE
	with open('tokens.json') as token_file:
		token_data = json.load(token_file)
		telegram_bot_token = token_data['telegram_bot_token']
		

	
	robot = bot.bot_main(telegram_bot_token)
    
	

if __name__ == "__main__":
	main()

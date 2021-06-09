from bot import BotEDT
from keep_alive import keep_alive
from os import getenv
from variables import channel, group_to_mention, MI_URLS, help_text

def main():
	keep_alive()
	bot = BotEDT(channel,group_to_role_mention,MI_URLS,help_text)
	bot.run(getenv("TOKEN"))

if __name__ == "__main__":
	main()

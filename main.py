from botedt import BotEDT
from keep_alive import keep_alive
from os import getenv
from helper_functs import current_timeint
from variables import prefix, channel, group_to_mention, MI_URLS, help_text
import logging


def main():
	keep_alive()

	logging.basicConfig(
		filename=f"log_{current_timeint()}.log",
		format="[%(asctime)s] %(levelname)s: %(message)s",
		encoding="utf-8",
		level=logging.DEBUG
	)

	bot = BotEDT(prefix, channel, group_to_mention, MI_URLS, help_text)
	bot.run(getenv("TOKEN"))

	logging.shutdown()


if __name__ == "__main__":
	main()

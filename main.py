from botedt import BotEDT
from keep_alive import keep_alive
from os import getenv
from variables import (
	prefix, channel, help_text,
	groups, nicknames, role_ids
)
import logging


def main():
	keep_alive()

	bot = BotEDT(
		prefix, channel, help_text,
		groups, nicknames, role_ids
	)
	bot.run(getenv("TOKEN"))
	bot.logger.warning("Shutdown!")
	logging.shutdown()


if __name__ == "__main__":
	main()

from botedt import BotEDT
from keep_alive import keep_alive
from os import getenv
from variables import (
	prefix, channel, nickname_to_id,
	group_to_mention, MI_groups, help_text
)
import logging


def main():
	keep_alive()

	bot = BotEDT(
		prefix, channel, nickname_to_id,
		group_to_mention, MI_groups, help_text
	)
	bot.run(getenv("TOKEN"))
	logging.shutdown()


if __name__ == "__main__":
	main()

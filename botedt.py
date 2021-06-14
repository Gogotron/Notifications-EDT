from discord.ext.commands import Bot
from discord.ext.tasks import loop
from bot_commands import bot_commands
from emploi_du_temps import fetch_combined
from links import get_link
from helper_functs import event_to_seconds, current_dateint
from time import time, sleep
import logging


class BotEDT(Bot):
	def __init__(self, prefix, channel, group_to_mention, urls, help_text):
		logging.info("Initialize bot.")
		super().__init__(command_prefix="$")

		logging.info("Adding commands to bot.")
		self.remove_command("help")
		for command in bot_commands:
			self.add_command(command)
		logging.info("Finished adding commands to bot.")

		self.channel = channel
		self.group_to_mention = group_to_mention
		self.urls = urls
		self.help_text = help_text
		self.schedule = []
		self.last_update = None

		self.check_for_event.start()

	async def on_ready(self):
		print(f"We have logged in as {self.user}.")
		logging.info(f"Bot is ready and logged in as {self.user}.")

	def event_available(self):
		return (
			len(self.schedule) != 0
			and event_to_seconds(self.schedule[0]) - time() < 15 * 60
		)

	def attempt_to_update(self):
		# A schedule is only valid for the day it was retrieved on.
		# Anytime after, the schedule is considered 'expired'.
		logging.info("Check if schedule expired.")
		if self.last_update != current_dateint():
			logging.info("Schedule expired, need a new one.")
			self.update_schedule()

	def update_schedule(self):
		logging.info("Updating schedule.")
		self.schedule = fetch_combined(self.urls, PI_filter=False)
		self.remove_past_events()
		# Validity corresponds to the date the schedule was obtained
		# because after a day the schedule is considered 'expired'.
		logging.info("Set schedule validity.")
		self.last_update = current_dateint()

	def remove_past_events(self):
		logging.info("Trimming schedule.")
		while self.event_available(self):
			del self.schedule[0]

	@loop(seconds=120)
	async def check_for_event(self):
		logging.info("Schedule loop iteration.")
		self.attempt_to_update()

		while self.event_available():
			logging.info("Can send event.")
			await self.send_event(self.schedule[0], notify=True)
			del self.schedule[0]
			sleep(3)

		if len(self.schedule) == 0:
			logging.info("No more events left.")
			self.check_for_event.stop()

	@check_for_event.before_loop
	async def before_check_for_event(self):
		print("Before loop")
		logging.info("Schedule loop starts.")
		self.update_schedule()
		logging.info("Wait for bot to log in.")
		await self.wait_until_ready()

	@check_for_event.after_loop
	async def after_check_for_event(self):
		print("After loop")
		logging.warning("Schedule loop is no longer running.")
		await self.client.get_channel(801041584870916118).send(
			"After loop: the program is no longer running.\n<@310836324766580738>"
		)

	def next_class(self, n, group_nickname):
		valid_groups = self.corresponding_groups(group_nickname)
		i = 0
		while n >= 0 and i < len(self.schedule):
			if self.schedule[i]["groups"]:
				for valid_g in valid_groups:
					if valid_g in self.schedule[i]["groups"]:
						n -= 1
						break
			i += 1
		return self.schedule[i - 1]

	async def send_event(self, e, notify=False, reply_to=None):
		logging.info("Sending event.")
		logging.debug(f"Event:{str(e)}")
		msg_txt = self.event_message(e, notify)
		logging.debug(f"Message:{msg_txt}")

		if reply_to is not None:
			logging.info("Sending event as a reply.")
			await reply_to.reply(msg_txt)
		else:
			logging.info("Sending event as a message.")
			message_to_publish = await self.get_channel(self.channel).send(msg_txt)
			logging.info("Publishing message.")
			await message_to_publish.publish()

	def event_message(self, e, notify):
		logging.info("Writing event message.")
		weekdays = ("Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi")

		if e["category"] in ('Examens Licences', 'Examens'):
			notify = False
		msg_txt = ""

		year, month, day = e['real_date']
		weekday = weekdays[int(e['day'])]
		module, category = e["module"], e["category"]
		msg_txt += (
			f"** *"
			f"{e['starttime']}-{e['endtime']}"
			f"  ─  {weekday}  ─  "
			f"{day}/{month}/{year}"
			f"* **\n"
		)
		if module[0] == "4":
			module = module.split(" ", maxsplit=1)[1]
		if module and category:
			msg_txt += f"**{module} ({category})**\n"
		if module:
			msg_txt += f"**{module}**\n"
		elif category:
			msg_txt += f"**{category}**\n"

		msg_txt += "```\n"
		room, staff, notes, groups = e["room"], e["staff"], e["notes"], e["groups"],
		if room:
			msg_txt += f"{room}\n"
		if staff:
			msg_txt += f"Prof: {', '.join(staff)}\n"
		if notes:
			msg_txt += f"Remarques: {notes}\n"
		mentions = []
		if groups:
			for group in groups:
				msg_txt += f"{group}\n"
				if group in self.group_to_mention:
					for role in self.group_to_mention[group]:
						if role not in mentions:
							mentions.append(role)
		msg_txt += "```"

		if len(mentions) != 0 and notify:
			msg_txt += ' '.join(mentions) + "\n"

		link = get_link(e)
		if link:
			msg_txt += f"{link}\n"

		return msg_txt

	def corresponding_groups(self, group_nickname):
		logging.info(f"Getting groups whose nickname is {group_nickname}.")
		if group_nickname == "ISI":
			return set(('CMI ISI201 GROUPE A1', ))
		if group_nickname == "CMI":
			return set(('CMI OPTIM 201', ))

		valid_groups = set(
			filter(
				lambda x: group_nickname in x.split(),
				list(self.group_to_mention.keys())[:-3]
			)
		)
		if len(group_nickname) > 1:
			valid_groups |= self.corresponding_groups(group_nickname[:-1])

		if len(valid_groups) == 0:
			logging.warning(f"Found no groups whose nickname is {group_nickname}.")
			return set(self.group_to_mention.keys())
		else:
			return valid_groups

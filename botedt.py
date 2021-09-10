from discord.ext.commands import Bot
from discord.ext.tasks import loop
from bot_commands import bot_commands
from emploi_du_temps import get_combined_schedule
from links import get_link
from helper_functs import event_to_seconds, current_dateint, current_timeint
from time import time, sleep
import logging


class BotEDT(Bot):
	def __init__(
		self,
		prefix: str,
		channel: int,
		nickname_to_id: dict,
		group_to_mention: dict,
		groups: list,
		help_text: str
	):
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.DEBUG)
		handler = logging.FileHandler(
			f"logs/log_{current_timeint()}.log", "w", "utf-8"
		)
		handler.setFormatter(logging.Formatter(
			"[%(asctime)s] %(levelname)s: %(message)s"
		))
		self.logger.addHandler(handler)

		self.logger.info("Initialize bot.")
		super().__init__(command_prefix="$")

		self.logger.info("Adding commands to bot.")
		self.remove_command("help")
		for command in bot_commands:
			self.add_command(command)
		self.logger.info("Finished adding commands to bot.")

		self.channel = channel
		self.nickname_to_id = nickname_to_id
		self.group_to_mention = group_to_mention
		self.groups = groups
		self.help_text = help_text
		self.schedule = []
		self.last_update = None

		self.check_for_event.start()

	async def on_ready(self):
		print(f"We have logged in as {self.user}.")
		self.logger.info(f"Bot is ready and logged in as {self.user}.")

	def event_available(self) -> bool:
		return (
			len(self.schedule) != 0
			and event_to_seconds(self.schedule[0]) - time() < 15 * 60
		)

	def attempt_to_update(self):
		# A schedule is only valid for the day it was retrieved on.
		# Anytime after, the schedule is considered 'expired'.
		# self.logger.info("Check if schedule expired.")
		if self.last_update != current_dateint():
			self.logger.info("Schedule expired, need a new one.")
			self.update_schedule()

	def update_schedule(self):
		self.logger.info("Updating schedule.")
		self.schedule = get_combined_schedule(self.groups)
		self.remove_past_events()
		# Validity corresponds to the date the schedule was obtained
		# because after a day the schedule is considered 'expired'.
		self.logger.info("Set schedule validity.")
		self.last_update = current_dateint()

	def remove_past_events(self):
		self.logger.info("Trimming schedule.")
		while self.event_available():
			del self.schedule[0]

	@loop(seconds=120)
	async def check_for_event(self):
		# self.logger.info("Schedule loop iteration.")
		self.attempt_to_update()

		while self.event_available():
			self.logger.info("Can send event.")
			await self.send_event(self.schedule[0], notify=True)
			del self.schedule[0]
			sleep(3)

		if len(self.schedule) == 0:
			self.logger.info("No more events left.")
			self.check_for_event.stop()

	@check_for_event.before_loop
	async def before_check_for_event(self):
		self.logger.info("Schedule loop starts.")
		self.update_schedule()
		self.logger.info("Wait for bot to log in.")
		await self.wait_until_ready()

	@check_for_event.after_loop
	async def after_check_for_event(self):
		self.logger.warning("Schedule loop is no longer running.")
		await self.client.get_channel(801041584870916118).send(
			"After loop: the program is no longer running.\n<@310836324766580738>"
		)

	def next_class(self, n: int, group_nickname: str):
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

	async def send_event(
		self,
		e: dict,
		notify: bool = False,
		reply_to: "context" = None
	):
		self.logger.info("Sending event.")
		self.logger.debug(f"Event:{str(e)}")
		msg_txt = self.event_message(e, notify)
		self.logger.debug(f"Message:{msg_txt!r}")

		if reply_to is not None:
			self.logger.info("Sending event as a reply.")
			await reply_to.reply(msg_txt)
		else:
			self.logger.info("Sending event as a message.")
			message_to_publish = await self.get_channel(self.channel).send(msg_txt)
			self.logger.info("Publishing message.")
			await message_to_publish.publish()

	def event_message(self, e: dict, notify: bool) -> str:
		self.logger.info("Writing event message.")
		weekdays = ("Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi")

		if e["category"] in ('Examens Licences', 'Examens'):
			notify = False
		msg_txt = ""

		year, month, day = e['date']
		weekday = weekdays[int(e['day'])]
		module, category = e["module"], e["category"]
		msg_txt += (
			f"** *"
			f"{e['starttime']}-{e['endtime']}"
			f"  ─  {weekday}  ─  "
			f"{day}/{month}/{year}"
			f"* **\n"
		)
		if module:
			if module[0] == "4":
				module = module.split(" ", maxsplit=1)[1]
			if category:
				msg_txt += f"**{module} ({category})**\n"
			else:
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
					role = self.group_to_mention[group]
					mentions.append(role)
		msg_txt += "```"

		if len(mentions) != 0 and notify:
			msg_txt += ' '.join(mentions) + "\n"

		link = get_link(e)
		if link:
			msg_txt += f"{link}\n"

		return msg_txt

	def corresponding_groups(self, group_nickname: str) -> tuple:
		self.logger.info(f"Getting groups whose nickname is {group_nickname}.")
		if group_nickname == 'ISI':
			group_name = 'ISI301A1'
		elif len(group_nickname) >= 2:
			group_name = group_nickname[:2]+'301A'+group_nickname[2:]
		valid_groups = tuple(filter(
			lambda x: x.startswith(group_name),
			list(self.group_to_mention.keys())
		))
		if len(valid_groups) == 0:
			self.logger.warning(f"Found no groups whose nickname is {group_nickname}.")
			return tuple(self.group_to_mention.keys())
		else:
			return valid_groups

from keep_alive import keep_alive
from discord import Client
from discord.ext.tasks import loop
from discord.utils import get
from os import getenv
from time import time, sleep

from emploi_du_temps import fetch_combined, URL_MINF_A, URL_MINF_B, URL_CMI_ISI, URL_CMI_OPTIM
from helper_functs import event_to_seconds, current_dateint
from links import get_link

weekdays = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
with open("help_text.txt", "r") as f:
	help_text = f.read().strip()

channel = 802640238664351826
roles = (
    "<@&802575166831067166>",  #A1
    "<@&802575212280807494>",  #A2
    "<@&802575231691915344>",  #A3
    "<@&802575247391064075>",  #A4
    "<@&802575284070514688>",  #A5
    "<@&802573383924449280>",  #A6
    "<@&802573021222928414>",  #B1
    "<@&802573125212045332>",  #B2
    "<@&802573213602283521>",  #B3
    "<@&802573271320887306>",  #B4
    "<@&802573341495132222>",  #B5
    "<@&802578798444675113>",  #ISI
    "<@&802579017102000158>",  #OPTIM
)
group_to_role = {
    'MINF201 SERIE A (Maths/Info)': roles[0:6],
    'MINF201 SERIE B (Maths/Info)': roles[6:11],
    'MINF201 GROUPE A1 (Maths/Info)': roles[0:1],
    'MINF201 GROUPE A2 (Maths/Info)': roles[1:2],
    'MINF201 GROUPE A3 (Maths/Info)': roles[2:3],
    'MINF201 GROUPE A4 (Maths/Info)': roles[3:4],
    'MINF201 GROUPE A5 (Maths/Info)': roles[4:5],
    'MINF201 GROUPE A6 (Maths/Info)': roles[5:6],
    'MINF201 GROUPE B1 (Maths/Info)': roles[6:7],
    'MINF201 GROUPE B2 (Maths/Info)': roles[7:8],
    'MINF201 GROUPE B4 (Maths/Info)': roles[9:10],
    'MINF201 GROUPE B5 (Maths/Info)': roles[10:11],
    'MINF201 GROUPE A11 (Maths/Info)': roles[0:1],
    'MINF201 GROUPE A12 (Maths/Info)': roles[0:1],
    'MINF201 GROUPE A21 (Maths/Info)': roles[1:2],
    'MINF201 GROUPE A22 (Maths/Info)': roles[1:2],
    'MINF201 GROUPE A31 (Maths/Info)': roles[2:3],
    'MINF201 GROUPE A32 (Maths/Info)': roles[2:3],
    'MINF201 GROUPE A41 (Maths/Info)': roles[3:4],
    'MINF201 GROUPE A42 (Maths/Info)': roles[3:4],
    'MINF201 GROUPE A51 (Maths/Info)': roles[4:5],
    'MINF201 GROUPE A52 (Maths/Info)': roles[4:5],
    'MINF201 GROUPE A61 (Maths/Info)': roles[5:6],
    'MINF201 GROUPE B11 (Maths/Info)': roles[6:7],
    'MINF201 GROUPE B12 (Maths/Info)': roles[6:7],
    'MINF201 GROUPE B21 (Maths/Info)': roles[7:8],
    'MINF201 GROUPE B22 (Maths/Info)': roles[7:8],
    'MINF201 GROUPE B41 (Maths/Info)': roles[9:10],
    'MINF201 GROUPE B42 (Maths/Info)': roles[9:10],
    'MINF201 GROUPE B51 (Maths/Info)': roles[10:11],
    'MINF201 GROUPE B52 (Maths/Info)': roles[10:11],
    'CMI ISI201 GROUPE A1': roles[11:12],
    'CMI OPTIM 201': roles[12:13],
}

client = Client()


@client.event
async def on_ready():
	print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if message.content == "$help":
		await message.reply(help_text)
	if message.content == "$ping":
		await message.reply(f"Pong: {round(client.latency*1000)}ms")
	if message.content.startswith("$next"):
		pieces = message.content.split()
		if len(pieces) > 3: return
		group_nickname, n = "", 0
		if len(pieces) >= 2: group_nickname = pieces[1].upper()
		if len(pieces) >= 3: n = int(pieces[2]) - 1
		if n < 0: return
		if group_nickname == "":
			if n >= len(schedule):
				e = schedule[-1]
			else:
				e = schedule[n]
		else:
			e = next_class(n, group_nickname)
		await send_to_discord(e, False, message)
	if message.content.startswith("$sendsend"):
		await client.get_channel(channel).send(message.content[10:])
	if message.content == "$minecraft":
		await message.author.add_roles(get(message.guild.roles,id=836949920488488970))
	if message.content == "$remove-minecraft":
		await message.author.remove_roles(get(message.guild.roles,id=836949920488488970))
		await message.reply("Tu ne devrais plus avoir le rôle 'Minecraft'.")
	if message.content == "$portal":
		await message.reply("Il est très bien le jeu, mais n'y a pas de rôle correspondant.")

async def send_to_discord(e, notify=True, reply_to=None):
	if e["category"] in ('Examens Licences', 'Examens'): notify = False
	msg_txt = ""

	year, month, day = e['real_date']
	msg_txt += f"** *{e['starttime']}-{e['endtime']}  ─  {weekdays[int(e['day'])]}  ─  {day}/{month}/{year}* **\n"
	if e["module"]:
		msg_txt += "**"
		module, category = e["module"], e["category"]
		msg_txt += module.split(" ", maxsplit=1)[1]
		if category:
			msg_txt += f" ({category})"
		msg_txt += "**\n"
	elif e["category"]:
		msg_txt += "**" + e["category"] + "**"

	msg_txt += "```\n"
	if e["room"]:
		msg_txt += e["room"] + "\n"
	if e["staff"]:
		msg_txt += f"Prof: {', '.join(e['staff'])}\n"
	if e["notes"]:
		msg_txt += f"Remarques: {e['notes']}\n"
	group_roles = []
	if e["groups"]:
		for group in e["groups"]:
			msg_txt += group + "\n"
			if group in group_to_role:
				for role in group_to_role[group]:
					if role not in group_roles:
						group_roles.append(role)
	msg_txt += "```"

	if len(group_roles) != 0 and notify:
		msg_txt += ' '.join(group_roles) + "\n"

	link = get_link(e)
	if link is not None:
		msg_txt += link + "\n"

	if reply_to is not None:
		await reply_to.reply(msg_txt)
	else:
		message_to_publish = await client.get_channel(channel).send(msg_txt)
		await message_to_publish.publish()


@loop(seconds=120)
async def check_for_event():
	check_for_update()

	global schedule
	while len(schedule) != 0 and event_to_seconds(
	    schedule[0]) - time() < 15 * 60:
		await send_to_discord(schedule[0], notify=True)
		del schedule[0]
		sleep(3)

	if len(schedule) == 0:
		check_for_event.stop()


@check_for_event.before_loop
async def before_check_for_event():
	print("Before loop")
	update_schedule()
	await client.wait_until_ready()


@check_for_event.after_loop
async def after_check_for_event():
	print("After loop")
	await client.get_channel(801041584870916118).send(
	    "After loop: the program is no longer running.\nFreak out!\n<@310836324766580738>"
	)
	await client.get_channel(801041584870916118).send(str(schedule[0]))


def check_for_update():
	global last_update
	if last_update != current_dateint():
		update_schedule()


def update_schedule():
	global schedule, last_update
	schedule = fetch_combined(urls, PI_filter=False)
	remove_past_events()
	last_update = current_dateint()


def remove_past_events():
	global schedule
	while len(schedule) != 0 and event_to_seconds(
	    schedule[0]) - time() < 15 * 60:
		del schedule[0]


def next_class(n, group_nickname):
	global schedule
	valid_groups = corresponding_groups(group_nickname)
	i = 0
	while n >= 0 and i < len(schedule):
		if schedule[i]["groups"]:
			for valid_g in valid_groups:
				if valid_g in schedule[i]["groups"]:
					n -= 1
					break
		i += 1
	return schedule[i - 1]


def corresponding_groups(group_nickname):
	if group_nickname == "ISI":
		return set(('CMI ISI201 GROUPE A1', ))
	if group_nickname == "CMI":
		return set(('CMI OPTIM 201', ))

	valid_groups = set(
	    filter(lambda x: group_nickname in x.split(),
	           list(group_to_role.keys())[:-3]))
	if len(group_nickname) > 1:
		valid_groups |= corresponding_groups(group_nickname[:-1])
	if len(valid_groups) == 0:
		return set(group_to_role.keys())
	else:
		return valid_groups


if __name__ == "__main__":
	urls = (URL_MINF_A, URL_MINF_B, URL_CMI_ISI, URL_CMI_OPTIM)

	check_for_event.start()
	keep_alive()
	client.run(getenv("TOKEN"))

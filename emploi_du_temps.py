import requests
from bs4 import BeautifulSoup as bs
from helper_functs import real_date, timeint, sort_schedule, remove_non_PI
from variables import PI_URLS, MI_URLS

def get_schedule(URL):
	page = requests.get(URL)
	soup = bs(page.content, 'html.parser')
	events = soup.find_all('event')

	return parse_events(events)

def parse_events(events):
	event_dictionnaries = []
	for event in events:
		edict = {}

		# Mandatory attribute
		edict["date"] = event["date"]
		# Mandatory tag
		edict["day"]		= event.day			.get_text()
		edict["starttime"]	= event.starttime	.get_text()
		edict["endtime"]	= event.endtime		.get_text()
		edict["category"]	= event.category	.get_text()
		edict["prettyweek"]	= event.prettyweeks	.get_text()
		# Optional values
		if event.resources.module:
			edict["module"] = event.resources.module.item.get_text()
		else: edict["module"] = None
		if event.resources.room:
			edict["room"] = event.resources.room.item.get_text()
		else: edict["room"] = None
		if event.notes:
			for br in event.notes.find_all('br'):
				br.replace_with("###")
			edict["notes"] = event.notes.get_text().replace("###"," ").strip()
		else: edict["notes"] = None
		# Optional list values
		if event.resources.group:
			edict["groups"]	= [
				i.get_text()
				for i in event.resources.group.find_all('item')]
		else: edict["groups"] = None
		if event.resources.staff:
			edict["staff"] = [
				i.get_text()
				for i in event.resources.staff.find_all('item')]
		else: edict["staff"] = None

		event_dictionnaries.append(edict)

	for event in event_dictionnaries:
		event["week"] = int(event["prettyweek"])
		event["start"] = tuple(map(int, event["starttime"].split(':')))
		event["end"] = tuple(map(int, event["endtime"].split(':')))
		event["real_date"] = real_date(event["date"], event["day"])
		event["timeint"] = timeint(event)

	return sorted_schedule(event_dictionnaries)

def fetch_combined(urls, PI_filter=False):
	combined_schedule = []
	for s in map(get_schedule,urls):
		for e in remove_non_PI(s) if PI_filter else s:
			if e not in combined_schedule:
				combined_schedule.append(e)
	return sorted_schedule(combined_schedule)

if __name__=="__main__":
	from helper_functs import print_event
	from time import time

	start = time()
	sche = fetch_combined(PI_URLS,PI_filter=True)
	print("Time:",time()-start)

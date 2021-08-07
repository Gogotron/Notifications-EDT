import requests
from bs4 import BeautifulSoup as bs
from helper_functs import (
	real_date,
	event_timeint,
	sorted_schedule,
	remove_non_PI
)


def get_schedule(url: str) -> list:
	page = requests.get(url)
	soup = bs(page.content, 'html.parser')
	events = soup.find_all('event')

	return parse_events(events)


def parse_events(events: list) -> list:
	event_dictionnaries = []
	for event in events:
		event_dictionnaries.append(parse_event(event))
	return sorted_schedule(event_dictionnaries)


def parse_event(event: "Tag") -> dict:
	# Mandatory tag
	edict = {
		"day":       event.day        .get_text(),
		"starttime": event.starttime  .get_text(),
		"endtime":   event.endtime    .get_text(),
		"category":  event.category   .get_text(),
		"week":      int(event.prettyweeks.get_text()),
		"module":    None,
		"room":      None,
		"notes":     None,
		"groups":    None,
		"staff":     None,
	}
	edict["start"]     = tuple(map(int, edict["starttime"].split(':')))
	edict["end"]       = tuple(map(int, edict["endtime"].split(':')))
	edict["real_date"] = real_date(event["date"], edict["day"])
	edict["start_int"] = event_timeint(edict, "start")
	edict["end_int"]   = event_timeint(edict, "end")
	edict["timeint"]   = event_timeint(edict)
	# Optional values
	if event.resources.module:
		edict["module"] = event.resources.module.item.get_text()
	if event.resources.room:
		edict["room"] = event.resources.room.item.get_text()
	if event.notes:
		for br in event.notes.find_all('br'):
			br.replace_with("###")
		edict["notes"] = event.notes.get_text().replace("###", " ").strip()
	# Optional list values
	if event.resources.group:
		edict["groups"] = [
			i.get_text()
			for i in event.resources.group.find_all('item')
		]
	if event.resources.staff:
		edict["staff"] = [
			i.get_text()
			for i in event.resources.staff.find_all('item')
		]

	return edict


def fetch_combined(urls: list, PI_filter: bool = False) -> list:
	combined_schedule = []
	for s in map(get_schedule, urls):
		for e in (remove_non_PI(s) if PI_filter else s):
			if e not in combined_schedule:
				combined_schedule.append(e)
	return sorted_schedule(combined_schedule)


if __name__ == "__main__":
	from time import time
	from variables import PI_URLS

	start = time()
	sche = fetch_combined(PI_URLS, PI_filter=True)
	print("Time:", time() - start)

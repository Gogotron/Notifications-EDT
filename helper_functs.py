from time import localtime, mktime, strptime, tzset
from os import environ
environ["TZ"] = 'CET'
tzset()


def timeint(year: int, month: int, day: int, hour: int, minute: int) -> int:
	return ((((year*100+month)*100 + day)*100+hour)*100 + minute)


def event_timeint(e: dict, interval_bound: str = 'start') -> int:
	date, time = e[interval_bound].split('T')
	year, month,  day    = map(int, date.split('-'))
	hour, minute, second = map(int, time.split(':'))
	return timeint(year, month, day, hour, minute)


def current_timeint() -> int:
	t = localtime()
	year, month, day = t.tm_year, t.tm_mon, t.tm_mday
	hour, minute = t.tm_hour, t.tm_min
	return timeint(year, month, day, hour, minute)


def current_dateint() -> int:
	return current_timeint() // 10000


def print_event(e: dict):
	print(
		"/".join(map(str, e["date"][::-1])),
		f"{e['starttime']}-{e['endtime']}"
	)
	if e["module"]:
		print(e["module"], end=' | ')
	print(e["category"])
	if e["room"]:
		print(e["room"])
	if e["groups"]:
		print(" | ".join(e["groups"]))
	if e["staff"]:
		print(", ".join(e["staff"]))
	if e["notes"]:
		print(e["notes"])


def sort_schedule(s: list):
	s.sort(key=lambda x: x["timeint"])


def sorted_schedule(s: list) -> list:
	return sorted(s, key=lambda x: x["timeint"])


def isnt_for_PI(e: dict) -> bool:
	notes = e["notes"] or ""
	return any((
		"ne concerne que les CMI" in notes,
		"uniquement les CMI" in notes,
		"TD en français" == notes,
		"Pour les non PI" == notes,
		"TDM en français pour les NON PI" == notes
	))


def is_for_PI(e: dict) -> bool:
	return not isnt_for_PI(e)


def remove_non_PI(L: list) -> filter:
	return filter(is_for_PI, L)


def event_to_seconds(e: dict) -> float:
	return mktime(strptime(str(e["timeint"]), "%Y%m%d%H%M"))

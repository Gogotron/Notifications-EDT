from time import localtime, mktime, strptime, tzset
from os import environ
environ["TZ"] = 'CET'
tzset()


def timeint(year: int, month: int, day: int, hour: int, minute: int) -> int:
	return ((((year*100+month)*100 + day)*100+hour)*100 + minute)


def event_timeint(e: dict, interval_bound: str = "start") -> int:
	year, month, day = e["real_date"]
	hour, minute = e[interval_bound]
	return timeint(year, month, day, hour, minute)


def current_timeint() -> int:
	t = localtime()
	year, month, day = t.tm_year, t.tm_mon, t.tm_mday
	hour, minute = t.tm_hour, t.tm_min
	return timeint(year, month, day, hour, minute)


def current_dateint() -> int:
	return current_timeint() // 10000


def leap(y: int) -> bool:
	return (y%4 == 0) and (not (y%100 == 0) or (y%400 == 0))


def real_date(a: str, b: str) -> tuple:
	day, month, year = map(int, a.split('/'))
	month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	if leap(year):
		month_lengths[1] = 29
	# Take into account the offset corresponding to the day of the week.
	offset = int(b)
	day += offset
	# Fix overflow from one month to the next, or one year to the next.
	month += day // month_lengths[month - 1]
	day %= month_lengths[month - 1]
	year += month // 12
	month %= 12
	return (year, month, day)


def text_to_time(a: str) -> tuple:
	return tuple(map(int, a.split(':')))


def print_event(e: dict):
	print(
		"/".join(map(str, e["real_date"][::-1])),
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

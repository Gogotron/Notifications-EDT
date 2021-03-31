def leap(y):
	return y%4==0 and (not y%100==0 or y%400==0)

def real_date(a,b):
	day, month, year = map(int,a.split('/'))
	if leap(year):
		month_lengths = [31,29,31,30,31,30,31,31,30,31,30,31]
	else:
		month_lengths = [31,28,31,30,31,30,31,31,30,31,30,31]
	plus = int(b)
	day += plus
	if day>month_lengths[month-1]:
		day %= month_lengths[month-1]
		month += 1
		if month>12:
			month %= 12
			year += 1
	return (year,month,day)

def text_to_time(a):
	return tuple(map(int,a.split(':')))

def timeint(e):
	year, month, day = e["real_date"]
	hour, minute = e["start"]
	return ((((year*100+month)*100+day)*100+hour)*100+minute)

def print_event(e):
	print("/".join(map(str,e["real_date"][::-1])), e["starttime"]+"-"+e["endtime"])
	if e["module"]: print(e["module"], end=' | ')
	print(e["category"])
	if e["room"]:	print(e["room"])
	if e["groups"]:	print(" | ".join(e["groups"]))
	if e["staff"]:	print(", ".join(e["staff"]))
	if e["notes"]:	print(e["notes"])

def sort_schedule(s):
	s.sort(key=lambda x:x["timeint"])

def sorted_schedule(s):
	return sorted(s,key=lambda x:x["timeint"])

def isnt_for_PI(e):
	notes = e["notes"] if e["notes"] else ""
	return any(("ne concerne que les CMI" in notes,
				"uniquement les CMI" in notes,
				"TD en français" == notes,
				"Pour les non PI" == notes,
				"TDM en français pour les NON PI" == notes))

def remove_non_PI(L):
	return filter(lambda e:not isnt_for_PI(e),L)

from time import time,localtime,mktime,strptime,tzset
from os import environ
environ["TZ"] = 'CET'
tzset()
def current_timeint():
	t = localtime() # UTC -> CTE
	year,month,day,hour,minute=t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min
	return ((((year*100+month)*100+day)*100+hour)*100+minute)
def current_dateint():
	return current_timeint()//100**2

def event_to_seconds(e):
	return mktime(strptime(str(e["timeint"]),"%Y%m%d%H%M")) # CTE -> UTC

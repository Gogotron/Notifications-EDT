from json import load
with open("links.json", "r", encoding="utf-8") as f:
	links = load(f)


def get_link(e: dict) -> str:
	e_dets = event_details(e)
	for l_details, link in links:
		if match(e_dets, l_details):
			return link
	return ""


def match(e_dets: dict, l_dets: dict) -> bool:
	for key in l_dets:
		if key not in e_dets or (e_dets[key] != l_dets[key]):
			return False
	return True


def event_details(e: dict) -> dict:
	return {
		"module":    e["module"],
		"category":  e["category"],
		"staff":     e["staff"][0] if e["staff"] else None,
		"weekday":   int(e["day"]),
		"starttime": e["starttime"],
	}

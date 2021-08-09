prefix = "$"


class WebApiURL:
	DOMAIN          = 'https://ukit.kbdev.io/Home/'
	GROUPS          = 'ReadResourceListItems'
	CALENDARDATA    = 'GetCalendarData'
	SIDEBAR         = 'GetSideBarEvent'


MI_groups = (
	'MA301A1', 'MA301A2', 'MA301A3',
	'MI301A1', 'MI301A2',
	'IN301A1', 'IN301A2', 'IN301A3', 'IN301A4', 'IN301A5',
)

channel = 802640238664351826
role_ids = (
	870986677823352882,  # MA1
	870987651115782154,  # MA2
	870987651115782154,  # MA3
	870988159746453507,  # MI1
	870988320254091296,  # MI2
	870988563825713152,  # IN1
	870988781661073418,  # IN2
	870988893653184562,  # IN3
	870988990558392340,  # IN4
	870989217994514482,  # IN5
)
role_mentions = tuple(map(lambda role_id: f"<@&{role_id}>", role_ids))

group_to_mention = {
	group: mention for group, mention in zip(MI_groups, role_mentions)
}

with open("help_text.txt", "r") as f:
	help_text = f.read().strip()

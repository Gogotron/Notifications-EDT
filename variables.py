prefix = "$"


channel = 802640238664351826

MI_groups = (
	'MA301A1', 'MA301A2', 'MA301A3',
	'MI301A1', 'MI301A2',
	'IN301A1', 'IN301A2', 'IN301A3', 'IN301A4', 'IN301A5',
	'ISI301A1',
)
group_nicknames = tuple(
	group[:2]+group[6:]
	for group in MI_groups[:-1]
) + ('ISI',)

role_ids = (
	870986677823352882,  # MA1
	870987651115782154,  # MA2
	870987951830605844,  # MA3
	870988159746453507,  # MI1
	870988320254091296,  # MI2
	870988563825713152,  # IN1
	870988781661073418,  # IN2
	870988893653184562,  # IN3
	870988990558392340,  # IN4
	870989217994514482,  # IN5
	802578798444675113,  # ISI
)
role_mentions = tuple(f"<@&{role_id}>" for role_id in role_ids)

nickname_to_id = {
	nickname: id for nickname, id in zip(group_nicknames, role_ids)
}
group_to_mention = {
	group: mention for group, mention in zip(MI_groups, role_mentions)
}

with open("help_text.txt", "r") as f:
	help_text = f.read().strip()

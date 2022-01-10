prefix = "$"


channel = 802640238664351826


groups = (
	'MF401A1 + PI', 'MF401A2', 'MF401A3 (MATH FOND)',
	'IGM401A1 (ING.MATHS)',
	'MI401A1', 'MI401A2',
	'INF401A1', 'INF401A2', 'INF401A3', 'INF401A4', 'INF401A5',
)

nicknames = tuple(
    section + sub_group[0]
    for section, sub_group in map(
        lambda x: x.split('401A'),
        groups
    )
)

role_ids = (
	921857411139129365,  # MF1
	921858354400333855,  # MF2
	921858400034381874,  # MF3
	921858449443258378,  # IGM1
	921858537804664882,  # MI1
	921858632646291517,  # MI2
	921858658017619998,  # INF1
	921858692759060482,  # INF2
	921858709620150282,  # INF3
	921858736690180096,  # INF4
	921858753656139776,  # INF5
)
assert len(role_ids)==len(set(role_ids))


with open("help_text.md", "r") as f:
	help_text = f.read().strip()

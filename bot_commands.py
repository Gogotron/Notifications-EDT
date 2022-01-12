from discord.ext.commands import command
from discord.utils import get


@command()
async def help(ctx):
	ctx.bot.logger.info(f"{ctx.author.name} issued `help` command.")
	await ctx.reply(ctx.bot.help_text)


@command()
async def ping(ctx):
	ctx.bot.logger.info(
		f"{ctx.author.name} issued `ping` command:"
		f" {round(ctx.bot.latency*1000)}ms"
	)
	await ctx.reply(f"Pong: {round(ctx.bot.latency*1000)}ms")


@command()
async def next(ctx, nickname="", n="1"):
	ctx.bot.logger.info(
		f"{ctx.author.name} issued `next` command,"
		f" with arguments `{nickname!r}` `{n!r}`."
	)
	nickname = nickname.upper()
	if len(ctx.bot.schedule) == 0:
		ctx.bot.logger.warning(
			"Schedule was empty, `next` command didn't return anything."
		)
		await ctx.reply("L'emploi du temps est vide.")
		return
	n = int(n) - 1
	if nickname == "":
		if n >= len(ctx.bot.schedule):
			e = ctx.bot.schedule[-1]
		else:
			e = ctx.bot.schedule[n]
	else:
		e = ctx.bot.next_class(n, nickname)
	await ctx.bot.send_event(e, False, ctx)


@command()
async def sendsend(ctx):
	if ctx.author.id == 310836324766580738:
		ctx.bot.logger.info(f"{ctx.author.name} issued `sendsend` command.")
		await ctx.bot.get_channel(ctx.bot.channel).send(ctx.message.content[10:])
	else:
		ctx.bot.logger.warning(
			f"{ctx.author.name} tried issuing the `sendsend` command."
		)


@command()
async def groupe(ctx, nickname):
	ctx.bot.logger.info(
		f"{ctx.author.name} issued `groupe` command,"
		f" with argument `{nickname!r}`."
	)
	nickname = nickname.upper()
	if nickname in ctx.bot.nicknames:
		role = get(ctx.guild.roles, id=ctx.bot.nickname_to_role_id[nickname])
		if role in ctx.author.roles:
			ctx.bot.logger.warning(
				f"{ctx.author.name} already had the `{nickname!r}` role."
			)
			await ctx.reply(f"Tu avais déjà le rôle '{nickname}'.")
		else:
			for other_role in map(
				lambda x: get(ctx.guild.roles, id=x),
				ctx.bot.role_ids
			):
				if other_role in ctx.author.roles:
					await ctx.author.remove_roles(other_role)
			await ctx.author.add_roles(role)
			await ctx.reply(
				f"Tu devrais maintenant avoir le rôle '{nickname}'."
			)
	else:
		ctx.bot.logger.warning(
			f"`{nickname!r}` has no corresponding role."
		)
		await ctx.reply(
            f"Le rôle '{nickname}' n'est pas disponible.\n"
            +'Les rôles disponibles sont:\n'
            +', '.join(ctx.bot.roles)
        )


@command()
async def donate(ctx):
	await ctx.reply(
		"Tu peux faire une donation à\n"
		"Monero: "
		"89dLqfcdyFQVSuNU6fK"
		"vAYcqXubj1ouqHWUZ7g"
		"rDjeXk2ggxrReBayjDP"
		"wHHGNbRfUKjq2iMYEHx"
		"DCsgNsYwACwg3j5jf2w"
	)


bot_commands = (
	help, ping, next, sendsend, groupe, donate
)

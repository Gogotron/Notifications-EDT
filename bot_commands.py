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
async def next(ctx, group_nickname="", n="1"):
	ctx.bot.logger.info(
		f"{ctx.author.name} issued `next` command,"
		f" with arguments `{group_nickname!r}` `{n!r}`."
	)
	group_nickname = group_nickname.upper()
	if len(ctx.bot.schedule) == 0:
		ctx.bot.logger.warning(
			"Schedule was empty, `next` command didn't return anything."
		)
		await ctx.reply("L'emploi du temps est vide.")
		return
	n = int(n) - 1
	if group_nickname == "":
		if n >= len(ctx.bot.schedule):
			e = ctx.bot.schedule[-1]
		else:
			e = ctx.bot.schedule[n]
	else:
		e = ctx.bot.next_class(n, group_nickname)
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
async def groupe(ctx, group_nickname):
	ctx.bot.logger.info(
		f"{ctx.author.name} issued `groupe` command,"
		f" with argument `{group_nickname!r}`."
	)
	group_nickname = group_nickname.upper()
	if group_nickname in ctx.bot.nickname_to_id:
		role = get(ctx.guild.roles, id=ctx.bot.nickname_to_id[group_nickname])
		if role in ctx.author.roles:
			ctx.bot.logger.warning(
				f"{ctx.author.name} already had the `{group_nickname!r}` role."
			)
			await ctx.reply(f"Tu avais déjà le rôle '{group_nickname}'.")
		else:
			for other_role in map(
				lambda x: get(ctx.guild.roles, id=x),
				ctx.bot.nickname_to_id.values()
			):
				if other_role in ctx.author.roles:
					await ctx.author.remove_roles(other_role)
			await ctx.author.add_roles(role)
			await ctx.reply(
				f"Tu devrais maintenant avoir le rôle '{group_nickname}'."
			)
	else:
		ctx.bot.logger.warning(
			f"`{group_nickname!r}` has no corresponding role."
		)
		await ctx.reply(f"Le rôle '{group_nickname}' n'est pas disponible.")


bot_commands = (
	help, ping, next, sendsend, groupe
)

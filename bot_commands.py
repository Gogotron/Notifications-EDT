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
		f" with arguments `{group_nickname}` `{n}`."
	)
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
	await ctx.bot.post_event(e, False, ctx)


@command()
async def sendsend(ctx):
	if ctx.author.id == 310836324766580738:
		ctx.bot.logger.info(f"{ctx.author.name} issued `sendsend` command.")
		await ctx.bot.get_channel(ctx.bot.channel).send(ctx.message.content[10:])
	else:
		ctx.bot.logger.warning(f"{ctx.author.name} tried issuing the `sendsend` command.")


@command()
async def minecraft(ctx):
	ctx.bot.logger.info(f"{ctx.author.name} issued `minecraft` command.")
	mc_role = get(ctx.guild.roles, id=836949920488488970)
	if mc_role not in ctx.author.roles:
		await ctx.author.add_roles(mc_role)
		await ctx.reply("Tu devrais maintenant avoir le rôle 'Minecraft'.")
	else:
		ctx.bot.logger.warning(f"{ctx.author.name} already had the 'Minecraft' role.")
		await ctx.reply("Tu avais déjà le rôle 'Minecraft'.")


@command("remove-minecraft")
async def remove_minecraft(ctx):
	ctx.bot.logger.info(f"{ctx.author.name} issued `remove-minecraft` command.")
	mc_role = get(ctx.guild.roles, id=836949920488488970)
	if mc_role in ctx.author.roles:
		await ctx.author.remove_roles(mc_role)
		await ctx.reply("Tu ne devrais plus avoir le rôle 'Minecraft'.")
	else:
		ctx.bot.logger.warning(f"{ctx.author.name} didn't have the 'Minecraft' role.")
		await ctx.reply("Tu n'avais pas le rôle 'Minecraft'.")


@command()
async def portal(ctx):
	ctx.bot.logger.info(f"{ctx.author.name} issued `portal` command.")
	await ctx.reply(
		"Il est très bien le jeu, mais n'y a pas de rôle correspondant."
	)


bot_commands = [
	help, ping, next, sendsend, minecraft, remove_minecraft, portal
]

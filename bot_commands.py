from discord.ext.commands import command
from discord.utils import get


@command()
async def help(ctx):
	await ctx.reply(ctx.bot.help_text)


@command()
async def ping(ctx):
	await ctx.reply(f"Pong: {round(ctx.bot.latency*1000)}ms")


@command()
async def next(ctx, group_nickname="", n="1"):
    n = int(n)-1
	if group_nickname == "":
		if n >= len(schedule):
			e = schedule[-1]
		else:
			e = schedule[n]
	else:
		e = next_class(n, group_nickname)
	await ctx.bot.post_event(e, False, ctx)


@command()
async def sendsend(ctx):
	await ctx.bot.get_channel(ctx.bot.channel).send(ctx.message.content[10:])


@command()
async def minecraft(ctx):
	await ctx.author.add_roles(get(ctx.guild.roles,id=836949920488488970))
	await ctx.reply("Tu devrais maintenant avoir le rôle 'Minecraft'.")


@command("remove-minecraft")
async def remove_minecraft(ctx):
	await ctx.author.remove_roles(get(ctx.guild.roles,id=836949920488488970))
	await ctx.reply("Tu ne devrais plus avoir le rôle 'Minecraft'.")


@command()
async def portal(ctx):
	await ctx.reply("Il est très bien le jeu, mais n'y a pas de rôle correspondant.")


bot_commands = [help,ping,next,sendsend,minecraft,remove_minecraft,portal]

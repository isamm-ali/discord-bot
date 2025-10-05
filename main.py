import discord
from discord.ext import commands
import logging
import os
from dotenv import load_dotenv
import webserver

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='-', intents=intents)

# ====================== Events ======================

@bot.event
async def on_ready():
    print(f"We have logged in as, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to our server {member.name}! ❤️")
    channel = bot.get_channel(1420432950779973632)
    await channel.send(f"{member.mention} Welcome to the server! We are happy to have you here. 🔥")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Bad words filter (skip commands)
    if not message.content.startswith(bot.command_prefix):
        bad_words = ["shit","fuck","bitch","lund","rape","nigger","nigga",
                     "chutiya","madarchod","chut","bhosdike","bsdk","gaandu",
                     "lode","cunt","pussy","dick","porn","sex","masturbate","cum","gandu","rapist","molest","randi","rand"]

        for word in bad_words:
            if word in message.content.lower():
                await message.delete()
                await message.channel.send(f"{message.author.mention}, please watch your language! ❌")
                break  # stop after first match

    # Process commands once
    await bot.process_commands(message)

# ====================== General Commands ======================

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}! 👋🏻")

@bot.command()
async def website(ctx):
    await ctx.send(f"Visit Club 404 website at: https://club404-page.vercel.app/ 🌐")

@bot.command()
async def linkedin(ctx):
    await ctx.send(f"Visit Club 404 LinkedIn page at: https://www.linkedin.com/company/109157269/admin/dashboard/ 🌐")

@bot.command()
async def twitter(ctx):
    await ctx.send(f"Visit Club 404 Twitter page at: https://x.com/club__404 🌐")

@bot.command()
async def instagram(ctx):
    await ctx.send(f"Visit Club 404 Instagram page at: https://www.instagram.com/club404aliah.official?igsh=MXEyNWVyYzk0dmJvaA== 🌐")

@bot.command()
async def core_members(ctx):
    await ctx.send(f"Core Members of Club 404 are: \n1. Ramij (President) \n2. Razaul Shoaib (Vice President) \n3. Sharabati Bose (Event Coordinator) \n4. Inzamam (Community Manager) \n5. Yousuf (Tech Lead) \n6. Saikat (Tech Lead) \n7. Karan (Tech Lead) \n8. Isam Ali (PR and Outreach - Discord) \n9. Raghib (PR and Outreach - Twitter/X) \n10. Hasnain (Ninja) \n11. Warisha (Ninja) \n12. Farhat (Ninja) \n13. Tapojyoti (Ninja) \nMore to Join... 🌟")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question, color=0x00ff00)
    embed.set_footer(text="React with 👍🏻 or 👎🏻 to vote!")
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍🏻")
    await poll_message.add_reaction("👎🏻")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"✅ Deleted {len(deleted) - 1} messages.", delete_after=2)


# ====================== Server Info ======================

@bot.command(name="serverinfo", aliases=["server", "server-info"])
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name} Info", color=0x3498db)
    embed.add_field(name="Owner", value=guild.owner, inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Created On", value=guild.created_at.strftime("%d %b %Y"), inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
    await ctx.send(embed=embed)

# ====================== Moderation Commands ======================

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f"🔒 {channel.mention} has been locked.")

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f"🔓 {channel.mention} has been unlocked.")

@bot.command(name="slowmode")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    if seconds < 0:
        return await ctx.send("❌ Slowmode time must be 0 or higher.")
    await channel.edit(slowmode_delay=seconds)
    if seconds == 0:
        await ctx.send(f"🐇 Slowmode disabled in {channel.mention}.")
    else:
        await ctx.send(f"🐢 Slowmode set to **{seconds} seconds** in {channel.mention}.")

@bot.command()
async def helpme(ctx):
    embed = discord.Embed(title="🤖 Club 404 Bot Commands", color=0x5865F2)
    embed.add_field(name="👋 General", value="-hello, -website, -linkedin, -instagram, -twitter", inline=False)
    embed.add_field(name="🧹 Moderation", value="-purge [n], -lock, -unlock, -slowmode [s]", inline=False)
    embed.add_field(name="📊 Fun", value="-poll [question]", inline=False)
    embed.add_field(name="ℹ️ Info", value="-serverinfo", inline=False)
    await ctx.send(embed=embed)

# ====================== Run Bot ======================

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)

import discord
from discord import app_commands
from discord.ext import tasks
from datetime import datetime
import re

from key import key
import gemini
import weather_forecast
import task

# botをインスタンス化
bot = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(bot)
GUILD_ID = discord.Object(id=748871577377964054)

# 1分毎に実行
@tasks.loop(seconds=60)
async def loop():
    await bot.wait_until_ready()
    
    now = datetime.now()
    if 
    

# /test
@tree.command(name="test",
              description="会話のテスト",
              guild = GUILD_ID)
@app_commands.describe(msg="テキスト")
async def add_reminder_command(interaction: discord.Interaction, msg: str):
    await interaction.response.defer()
    res = gemini.talk(msg)
    await interaction.followup.send(content = res, ephemeral = True)

# メンションに反応
@bot.event
async def on_message(msg: discord.Message):
    if msg.author == bot.user:
        return
    if msg.mentions.count(bot.user) == 0:
        return
    fix_msg = re.sub("<.*>", "", msg.content)
    res = gemini.talk(fix_msg)
    await msg.reply(content = res)

# botの準備完了時にメッセージ 
@bot.event
async def on_ready():
    await tree.sync(guild=GUILD_ID)
    loop.start()
    print(bot.user.name + " is ready!")


# tokenを読み込んでbotを起動
bot.run(key.DISCORD_BOT_TOKEN)
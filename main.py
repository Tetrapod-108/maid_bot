import discord
from discord import app_commands
from discord.ext import tasks
from datetime import datetime
import re

from key import key
import gemini
#import weather_forecast
import task

# botをインスタンス化
bot = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(bot)
GUILD_ID = discord.Object(id=748871577377964054)

# 1分毎に実行
@tasks.loop(seconds=60)
async def loop():
    await bot.wait_until_ready()
    
    # タスクリストをリマインド
    now = datetime.now()
    if (now.hour == 21 and now.minute == 0) or (now.hour == 7 and now.minute == 0)or (now.hour==9 and now.minute==34):
        msg = task.remind_task(now)
        ch = bot.get_channel(1319690391251062835)
        await ch.send(content="<@702791485409722388>\n"+msg)
    

# /add_taskコマンド
@tree.command(name="add_task",
              description="タスクをリストに追加する",
              guild=GUILD_ID)
@app_commands.describe(name="タスクの名前", date="日", time="時間")
async def add_task_command(interaction: discord.Interaction, name: str, date:str = None, time:str = None):
    await interaction.response.defer()
    format1 = r"([0-9]{1,2})/([0-9]{1,2})"
    format2 = r"([0-9]{1,2}):([0-9]{1,2})"
    if re.fullmatch(format1, date) == None and re.fullmatch(format2, time) == None:
        msg = gemini.talk("マスターに指示が間違っていることを伝えてください", False)
    elif date == None or (date == None and time == None):
        task.add_task(name, date, time)
        msg = gemini.talk(f"「{name}」のタスクをリストに追加してくれる？")
    else:
        task.add_task(name, date, time)
        msg = gemini.talk(f"「{name}」のタスクをリストに追加してくれる？")
    await interaction.followup.send(content = msg, ephemeral = True)

# /show_taskコマンド
@tree.command(name="show_task",
              description="タスクリストを表示する",
              guild=GUILD_ID)
@app_commands.describe()
async def show_task_command(interaction: discord.Interaction):
    await interaction.response.defer()
    now = datetime.now()
    msg = task.remind_task(now)
    ch = bot.get_channel(1319690391251062835)
    await ch.send(content="<@702791485409722388>\n"+msg)

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
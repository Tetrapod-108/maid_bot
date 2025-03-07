import discord
from discord import app_commands
from discord.ext import tasks
from discord.ext import commands
from datetime import datetime
import re

import key
import gemini
#import weather_forecast
import task
import reminder

# botをインスタンス化
bot = commands.Bot(command_prefix="", intents=discord.Intents.all())
tree = bot.tree
GUILD_ID = discord.Object(id=748871577377964054)

# 1分毎に実行
@tasks.loop(seconds=60)
async def loop():
    await bot.wait_until_ready()
    
    # タスクリストをリマインド
    now = datetime.now()
    #now = datetime(year=2025, month=1, day=12, hour=7, minute=0)
    if (now.hour == 21 and now.minute == 0) or (now.hour == 7 and now.minute == 0):
        now_date = datetime.now().strftime("%m月%d日%A %H:%M")
        task_list = task.remind_task(True)
        if task_list == "タスク無し":
            msg = gemini.talk(f"マスターへの挨拶、簡単な気遣いの言葉、という順でマスターにとくに予定がないことを通知してください。今は{now_date}なので、適した挨拶をしてください。また、明日の最高気温は6℃です。言及してなくても構いません。")
        else:
            msg = gemini.talk(f"「{task_list}」のようなタスクがあります。マスターへの簡単な挨拶、箇条書きで書いたタスクの一覧、簡単な気遣いの一文、という流れでマスターに予定をリマインドしてください。また、明日の最高気温は6℃です。今は{now}なので、適した挨拶、注意喚起をしてください。また、文の間に1行空けないでください。")
        ch = bot.get_channel(1319690391251062835)
        await ch.send(content="<@702791485409722388>\n"+msg)

    # リマインダーをリマインド
    msg = reminder.fetch_reminder(now.strftime("%Y-%m-%d %H:%M"))
    if msg != None:
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
    if date == None or time == None:
        msg = task.add_task(name, date, time)
    elif re.fullmatch(format1, date) == None and re.fullmatch(format2, time) == None:
        msg = gemini.talk("マスターにされた指示が間違っていることを伝えてください", False)
    elif date == None or (date == None and time == None):
        msg = task.add_task(name, date, time)
    else:
        msg = task.add_task(name, date, time)
    await interaction.followup.send(content = msg, ephemeral = True)


# /complete_taskコマンド
@tree.command(name="complete_task",
              description="完了したタスクをリストから削除する",
              guild=GUILD_ID)
@app_commands.describe(name="タスクの名前")
async def remove_task_command(interaction: discord.Interaction, name: str):
    await interaction.response.defer()
    msg = task.remove_task(name)
    await interaction.followup.send(content = msg, ephemeral = True)


# /show_taskコマンド
@tree.command(name="show_task",
              description="タスクリストを表示する",
              guild=GUILD_ID)
@app_commands.describe()
async def show_task_command(interaction: discord.Interaction):
    await interaction.response.defer()
    now = datetime.now()
    msg = task.remind_task(False, now)
    await interaction.followup.send(content = "<@702791485409722388>\n"+msg, ephemeral = True)


# /add_reminderコマンド
@tree.command(name="add_reminder",
              description="リマインダーを設定する",
              guild=GUILD_ID)
@app_commands.describe(message="リマインドの内容", time="リマインドする時間")
async def add_task_command(interaction: discord.Interaction, message:str, time:str):
    await interaction.response.defer()
    reminder.add_reminder(message, time)
    msg = "aaa"
    await interaction.followup.send(content = msg, ephemeral = True)


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
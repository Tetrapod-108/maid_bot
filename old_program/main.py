import discord
from discord import app_commands
from discord.ext import tasks
from discord.ext import commands
from datetime import datetime
import re

import config.key as key
import old_program.gemini as gemini
#import weather_forecast
import old_program.task as task
import old_program.reminder as reminder

# botをインスタンス化
bot = commands.Bot(command_prefix="", intents=discord.Intents.all())
tree = bot.tree
GUILD_ID = discord.Object(id=748871577377964054)

RESPONSE_MODE = 0
response_mode_timer = 0

# 1分毎に実行
@tasks.loop(seconds=60)
async def loop():
    global RESPONSE_MODE
    global response_mode_timer
    await bot.wait_until_ready()
    
    # タスクリストをリマインド
    now = datetime.now()
    #now = datetime(year=2025, month=3, day=22, hour=21, minute=0)
    if (now.hour == 21 and now.minute == 0) or (now.hour == 7 and now.minute == 0):
        now_date = datetime.now().strftime("%m月%d日%A %H:%M")
        task_list = task.remind_task(True)
        if task_list == "タスク無し":
            msg = gemini.talk(f"[システム: 時間:{now_date}] マスターへの挨拶、簡単な気遣いの言葉、という順でマスターにとくに予定がないことを通知してください。与えられた情報に適した挨拶をしてください。")
        else:
            msg = gemini.talk(f"[システム: 時間:{now_date}] マスターが取り組むべきタスクは以下のようになっています。「{task_list}」マスターへの簡単な挨拶、簡単な気遣いの一文、タスクについての簡単なまとめの一文、という流れでマスターに話してください。与えられた情報に適した挨拶、注意喚起をしてください。")
            msg = "<@702791485409722388>\n" + msg + "\n\n" + task_list
        ch = bot.get_channel(1319690391251062835)
        await ch.send(content=msg)

    # リマインダーをリマインド
    msg = reminder.fetch_reminder(now.strftime("%Y-%m-%d %H:%M"))
    if msg != None:
        ch = bot.get_channel(1352610162430578710)
        await ch.send(content="<@702791485409722388>\n"+msg)

    # RESPONSE_MODEの処理
    if response_mode_timer > 0:
        response_mode_timer -= 1
    elif response_mode_timer == 0:
        RESPONSE_MODE = 0


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
        msg = gemini.talk("マスターから受けた指示が間違っていることを伝えてください", False)
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
    task_list = task.remind_task(True)
    msg = gemini.talk(f"[システム: 現在の時間:{now} 注意:各文の間に1行空ける必要はありません]「{task_list}」のようなタスクがあります。マスターへの簡単な挨拶、簡単な気遣いの一文、タスクについての簡単なまとめ、という流れでマスターに話してください。与えられた情報に適した挨拶、注意喚起をしてください。")
    msg = "<@702791485409722388>\n" + msg + "\n\n" + task_list
    await interaction.followup.send(content = msg, ephemeral = True)


# /add_reminderコマンド
@tree.command(name="add_reminder",
              description="リマインダーを設定する",
              guild=GUILD_ID)
@app_commands.describe(time="リマインドする時間", message="リマインドの内容")
async def add_task_command(interaction: discord.Interaction, time:str, message:str):
    await interaction.response.defer()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rm_time = reminder.add_reminder(message, time)
    msg = gemini.talk(f"[システム: 現在の時間:{now} 注意:必ずしも絶対時間を伝える必要はありません、現在の時間を基準に〇日後、〇分後、のような時間表現を用いても大丈夫です、返答に数字を含める際は必ず半角を使ってください] マスターに、{rm_time}に「{message}」と通知してください")
    await interaction.followup.send(content = msg, ephemeral = True)


@bot.event
async def on_message(msg: discord.Message):
    global RESPONSE_MODE
    global response_mode_timer
    if msg.author == bot.user:
        return
    
    if RESPONSE_MODE == 1:
        now_date = datetime.now().strftime("%Y/%m/$d %H:%M")
        res = gemini.talk(f"[システム: 現在の時刻:{now_date}]" + msg.content)
        await msg.reply(content = res)
        response_mode_timer = 5
        return

    #if msg.mentions.count(bot.user) == 0:
    #    return
    if msg.channel.id != 1319690391251062835:
        print("aaa")
        return
    
    # メンションに反応
    #fix_msg = re.sub("<.*>", "", msg.content)
    now_date = datetime.now().strftime("%Y/%m/%d %H:%M")
    res = gemini.talk(f"[システム: 現在の時刻:{now_date}]" + msg.content)
    RESPONSE_MODE = 1
    response_mode_timer = 5
    await msg.reply(content = res)


# botの準備完了時にメッセージ 
@bot.event
async def on_ready():
    await tree.sync(guild=GUILD_ID)
    loop.start()
    print(bot.user.name + " is ready!")


# tokenを読み込んでbotを起動
bot.run(key.DISCORD_BOT_TOKEN)
import discord
from discord import app_commands
from discord.ext import tasks
from datetime import datetime

from key import key


# botをインスタンス化
bot = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(bot)
GUILD_ID = discord.Object(id=748871577377964054)

# 1分毎に実行
@tasks.loop(seconds=60)
async def loop():
    await bot.wait_until_ready()
    now = datetime.now()


# /add_reminderコマンド
@tree.command(name="add_reminder",
              description="リマインダーを作成するよ",
              guild = GUILD_ID)
@app_commands.describe(date="17:17とか1h5mみたいに指定してね", msg="リマインドしたいメッセージを入力してね")
async def add_reminder_command(interaction: discord.Interaction, date: str, msg: str):
    print("a")


# botの準備完了時にメッセージ 
@bot.event
async def on_ready():
    await tree.sync(guild=GUILD_ID)
    loop.start()
    print(bot.user.name + " is ready!")


# tokenを読み込んでbotを起動
bot.run(key.DISCORD_BOT_TOKEN)
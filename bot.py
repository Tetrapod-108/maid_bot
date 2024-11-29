import discord
from discord import app_commands
from discord.ext import tasks
from datetime import datetime


# botをインスタンス化
bot = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(bot)
ALL_GUILD_ID = [
  discord.Object(id=748871577377964054),
  discord.Object(id=1006904944873443412)
]
GUILD_ID1 = discord.Object(id=748871577377964054)


# 1分毎に実行
@tasks.loop(seconds=60)
async def loop():
  await bot.wait_until_ready()

  # reminder.csvを確認する
  now = datetime.now()
  rem_db = reminder.ReminderDatabase("reminder.csv")
  list = rem_db.fetch(now)
  for i in range(0, len(list)):
    ch = bot.get_channel(int(list[i].channel))
    await ch.send(content = f"<@{list[i].user}> {list[i].message}")


# /add_reminderコマンド
@tree.command(name="add_reminder",
              description="リマインダーを作成するよ",
              guilds = ALL_GUILD_ID)
@app_commands.describe(date="17:17とか1h5mみたいに指定してね", msg="リマインドしたいメッセージを入力してね")
async def add_reminder_command(interaction: discord.Interaction, date: str, msg: str):
  await interaction.response.defer()
  rem=reminder.Reminder(interaction.user.id, date, str(interaction.guild_id), str(interaction.channel_id), msg, date_calc=True)
  if rem.user == "-1":
    await interaction.followup.send(content = "適切な時間を入力してね！", ephemeral = True)
    return
  rem_db = reminder.ReminderDatabase("reminder.csv")
  rem_db.add(rem)
  time = rem.unix()
  await interaction.followup.send(content = "<t:" + str(time) + ">にリマインドを設定したよ！")
  return


# botの準備完了時にメッセージ 
@bot.event
async def on_ready():
  for i in range(0, len(ALL_GUILD_ID)):
    #tree.clear_commands(guild=ALL_GUILD_ID[i])
    a = await tree.sync(guild=ALL_GUILD_ID[i])
  loop.start()
  print(a)
  print(bot.user.name + " is ready!")


# tokenを読み込んでbotを起動
token = key.
bot.run(token)

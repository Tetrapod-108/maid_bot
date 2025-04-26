import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands

from features import task_list

import re

class TaskListCog(commands.Cog):
    # コンストラクタ
    def __init__(self, bot):
        self.bot = bot
    
    # タスクリストをリマインド
    @tasks.loop(seconds=60)
    async def remind_task_list():
        pass

    # /add_taskコマンド
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
    
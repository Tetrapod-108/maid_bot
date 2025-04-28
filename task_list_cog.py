import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands

from features.task_list import task_repository
from features.task_list import task
from features.gemini import gemini_chat_service

import re
import datetime
from pathlib import Path


class TaskListCog(commands.Cog):
    # コンストラクタ
    def __init__(self, bot, task_repo_file_path, gemini_api_key, prompt_path, history_file_path):
        self.bot = bot
        self.task_repo = task_repository.TaskRepository(task_repo_file_path)
        self.gemini_service = gemini_chat_service.GeminiChatService(api_key=gemini_api_key, prompt_path=prompt_path, history_file_path=history_file_path)
        self.remind_task_list.start()


    # タスクリストをリマインド
    @tasks.loop(seconds=60)
    async def remind_task_list(self):
        now = datetime.datetime.now()
        #now = datetime.datetime(year=2025, month=4, day=28, hour=21, minute=0)
        if (now.hour == 21 and now.minute == 0) or (now.hour == 7 and now.minute == 0):
            task_list = self.task_repo.get_all()
            msg = ""
            for task in task_list:
                msg += f"・{task.format_to_str()}\n"
            self.gemini_service.gen_meta_data()
            msg2 = self.gemini_service.talk(system_msg=f"マスターが取り組むべき「{msg}」のようなタスクがあります。簡単な挨拶、簡単な気遣いの一文、タスクについての総括、という流れでマスターに話してください。リストの全体を表示する必要はありません。現在時刻に適した挨拶をしてください。例)おはようございます、マスター。残っているタスクは集中力が必要なものが多いです。適宜休憩を挟むと良いかと思います。")
            ch = self.bot.get_channel(1319690391251062835)
            await ch.send(content="<@702791485409722388>\n" + msg2 + "\n\n" + msg)


    # /add_taskコマンド
    @app_commands.command(name = "add_task", description="タスクをリストに追加する")
    @app_commands.describe(name="タスクの名前", date="日", time="時間")
    async def add_task(self, interaction: discord.Interaction, name: str, date:str = None, time:str = None):
        await interaction.response.defer()
        format1 = r"([0-9]{1,2})/([0-9]{1,2})"
        format2 = r"([0-9]{1,2}):([0-9]{1,2})"
        if date == None or time == None:
            new_task = task.Task(name)
            self.task_repo.add(task=new_task)
            self.gemini_service.gen_meta_data()
            msg = self.gemini_service.talk(system_msg=f"タスクリストに「{new_task.format_to_str()}」を追加してください。また、追加したタスクに触れて会話してください。リストの全体を表示する必要はありません。")
        elif re.fullmatch(format1, date) == None and re.fullmatch(format2, time) == None:
            msg = self.gemini_service.talk(system_msg="マスターから受けた指示が間違っていることを伝えてください")
        elif date == None or (date == None and time == None):
            new_task = task.Task(name, date, time)
            self.task_repo.add(task=new_task)
            self.gemini_service.gen_meta_data()
            msg = self.gemini_service.talk(system_msg=f"マスターのタスクリストに「{new_task.format_to_str()}」を追加し、その旨をマスターに伝えてください。リストの全体を表示する必要はありません。")
        else:
            new_task = task.Task(name, date, time)
            self.task_repo.add(task=new_task)
            self.gemini_service.gen_meta_data()
            msg = self.gemini_service.talk(system_msg=f"マスターのタスクリストに「{new_task.format_to_str()}」を追加し、その旨をマスターに伝えてください。リストの全体を表示する必要はありません。")
        await interaction.followup.send(content = msg, ephemeral = True)


    # /complete_taskコマンド
    @app_commands.command(name = "complete_task", description="タスクをリストから削除")
    @app_commands.describe(name="タスクの名前")
    async def remove_task_command(self, interaction: discord.Interaction, name: str):
        await interaction.response.defer()
        try:
            self.task_repo.remove(name)
            self.gemini_service.gen_meta_data()
            msg = self.gemini_service.talk(system_msg=f"マスターのタスクリストから「{name}」を追加し、その旨をマスターに伝えてください。リストの全体を表示する必要はありません。")
            await interaction.followup.send(content = msg, ephemeral = True)
        except Exception as e:
            self.gemini_service.gen_meta_data()
            msg = self.gemini_service.talk(system_msg=f"マスターに対して、受けた指示が間違っていたことを伝えてください。")
            await interaction.followup.send(content = msg, ephemeral = True)


    # /show_taskコマンド
    @app_commands.command(name = "show_task", description="タスクリストを表示")
    @app_commands.describe()
    async def show_task_command(self, interaction: discord.Interaction):
        await interaction.response.defer()
        task_list = self.task_repo.get_all()
        msg = ""
        for task in task_list:
            msg += f"・{task.format_to_str()}\n"
        self.gemini_service.gen_meta_data()
        msg2 = self.gemini_service.talk(system_msg=f"マスターが取り組むべき「{msg}」のようなタスクがあります。簡単な挨拶、簡単な気遣いの一文、タスクについての総括、という流れでマスターに話してください。リストの全体を表示する必要はありません。現在時刻に適した挨拶をしてください。例)おはようございます、マスター。残っているタスクは集中力が必要なものが多いです。適宜休憩を挟むと良いかと思います。")
        await interaction.followup.send(content = "<@702791485409722388>\n" + msg2 + "\n\n" + msg, ephemeral = True)
 

if __name__ == "__main__":
    task_list_cog = TaskListCog(bot="bot", task_repo_file_path=f"{Path(__file__).parent}/json/task.json")
    #for task in task_list_cog.task_repo.get_all():
    #    print(task.name)
    task_list_cog.remind_task_list()
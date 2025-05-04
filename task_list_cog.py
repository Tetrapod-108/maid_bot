import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
from discord.ui import Select
from discord import SelectOption

from features.task_list import task_repository
from features.task_list import task
from features.gemini import gemini_chat_service
from features.multi_guild import guild_data_repository
from features.multi_guild import guild_data

import re
import datetime
from pathlib import Path


class TaskListCog(commands.Cog):
    # コンストラクタ
    def __init__(self, bot, task_repo_file_path, gemini_api_key, prompt_path, history_file_path, guild_file_path):
        self.bot = bot
        self.task_repo = task_repository.TaskRepository(task_repo_file_path)
        self.gemini_service = gemini_chat_service.GeminiChatService(api_key=gemini_api_key, prompt_path=prompt_path, history_file_path=history_file_path)
        self.remind_task_list.start()
        self.guild_repo = guild_data_repository.GuildDataRepository(file_path=guild_file_path)


    # タスクリストをリマインド
    @tasks.loop(seconds=60)
    async def remind_task_list(self):
        now = datetime.datetime.now()
        #now = datetime.datetime(year=2025, month=4, day=28, hour=21, minute=0)
        for guild_data in self.guild_repo.get_data():
            if (now.hour == guild_data.h1 and now.minute == guild_data.m1) or (now.hour == guild_data.h2 and now.minute == guild_data.m2):
                self.task_repo.edit_task_path(guild_id=guild_data.guild_id)
                task_list = self.task_repo.get_all()
                if task_list == []:
                    msg2 = self.gemini_service.talk(guild_id=guild_data.guild_id, system_msg=f"マスターに、簡単な挨拶、簡単な気遣いの一文、タスクがすべて終わっていることを伝える、という流れでマスターに話してください。リストの全体を表示する必要はありません。現在時刻に適した挨拶をしてください。例)おはようございます、マスター。現在取り組むべきタスクはありません。お疲れ様でした。")
                    ch = self.bot.get_channel(guild_data.ch_id)
                    await ch.send(content=f"<@{guild_data.user_id}>\n" + msg2)
                    return 
                msg = ""
                for task in task_list:
                    msg += f"・{task.format_to_str()}\n"
                self.gemini_service.gen_meta_data()
                msg2 = self.gemini_service.talk(guild_id=guild_data.guild_id, system_msg=f"マスターが取り組むべき「{msg}」のようなタスクがあります。簡単な挨拶、簡単な気遣いの一文、タスクについての総括、という流れでマスターに話してください。リストの全体を表示する必要はありません。現在時刻に適した挨拶をしてください。例)おはようございます、マスター。残っているタスクは集中力が必要なものが多いです。適宜休憩を挟むと良いかと思います。")
                ch = self.bot.get_channel(guild_data.ch_id)
                await ch.send(content=f"<@{guild_data.user_id}>\n" + msg2 + "\n\n" + msg)

    @remind_task_list.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()


    # /add_taskコマンド
    @app_commands.command(name = "add_task", description="タスクをリストに追加する")
    @app_commands.describe(name="タスクの名前", date="日", time="時間")
    async def add_task(self, interaction: discord.Interaction, name: str, date:str = None, time:str = None):
        await interaction.response.defer()
        format1 = r"([0-9]{1,2})/([0-9]{1,2})"
        format2 = r"([0-9]{1,2}):([0-9]{1,2})"
        if date == None or time == None:
            new_task = task.Task(name)
            self.task_repo.edit_task_path(guild_id=interaction.guild_id)
            self.task_repo.add(task=new_task)
            self.gemini_service.gen_meta_data()
            msg = self.gemini_service.talk(guild_id=interaction.guild_id, system_msg=f"タスクリストに「{new_task.format_to_str()}」を追加してください。また、追加したタスクに触れて会話してください。リストの全体を表示する必要はありません。")
        elif re.fullmatch(format1, date) == None and re.fullmatch(format2, time) == None:
            self.gemini_service.gen_meta_data()
            msg = self.gemini_service.talk(guild_id=interaction.guild_id, system_msg="マスターから受けた指示が間違っていることを伝えてください")
        elif date == None or (date == None and time == None):
            new_task = task.Task(name, date, time)
            self.task_repo.edit_task_path(guild_id=interaction.guild_id)
            self.task_repo.add(task=new_task)
            self.gemini_service.gen_meta_data()
            msg = self.gemini_service.talk(guild_id=interaction.guild_id, system_msg=f"マスターのタスクリストに「{new_task.format_to_str()}」を追加し、その旨をマスターに伝えてください。リストの全体を表示する必要はありません。")
        else:
            new_task = task.Task(name, date, time)
            self.task_repo.edit_task_path(guild_id=interaction.guild_id)
            self.task_repo.add(task=new_task)
            self.gemini_service.gen_meta_data()
            msg = self.gemini_service.talk(guild_id=interaction.guild_id, system_msg=f"マスターのタスクリストに「{new_task.format_to_str()}」を追加し、その旨をマスターに伝えてください。リストの全体を表示する必要はありません。")
        await interaction.followup.send(content = msg, ephemeral = True)


    # /complete_taskコマンド
    @app_commands.command(name = "complete_task", description="タスクをリストから削除")
    async def remove_task_command(self, interaction: discord.Interaction):
        await interaction.response.defer()
        task_list = []
        for task in self.task_repo.get_all():
            task_list.append(task.name)
        view = TaskView(20, interaction, task_list)
        name = ""
        try:
            self.task_repo.remove(name)
            self.gemini_service.gen_meta_data()
            msg = self.gemini_service.talk(guild_id=interaction.guild.id, system_msg=f"マスターのタスクリストから「{name}」を追加し、その旨をマスターに伝えてください。リストの全体を表示する必要はありません。")
            await interaction.followup.send(content = msg, ephemeral = True)
        except Exception as e:
            self.gemini_service.gen_meta_data()
            msg = self.gemini_service.talk(guild_id=interaction.guild_id, system_msg=f"マスターに対して、受けた指示が間違っていたことを伝えてください。")
            await interaction.followup.send(content = msg, ephemeral = True)


    # /show_taskコマンド
    @app_commands.command(name = "show_task", description="タスクリストを表示")
    @app_commands.describe()
    async def show_task_command(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.task_repo.edit_task_path(interaction.guild_id)
        task_list = self.task_repo.get_all()
        msg = ""
        for task in task_list:
            msg += f"・{task.format_to_str()}\n"
        self.gemini_service.gen_meta_data()
        msg2 = self.gemini_service.talk(guild_id=interaction.guild_id, system_msg=f"マスターが取り組むべき「{msg}」のようなタスクがあります。簡単な挨拶、簡単な気遣いの一文、タスクについての総括、という流れでマスターに話してください。リストの全体を表示する必要はありません。現在時刻に適した挨拶をしてください。例)おはようございます、マスター。残っているタスクは集中力が必要なものが多いです。適宜休憩を挟むと良いかと思います。")
        await interaction.followup.send(content = "<@702791485409722388>\n" + msg2 + "\n\n" + msg, ephemeral = True)
 

# タスクの削除するとき用のView
class TaskView(discord.ui.View):
    def __init__(self, timeout, interaction: discord.Interaction, task_list):
        super().__init__(timeout=timeout)
        self.interaction = interaction
        self.options = []
        for task in task_list:
            self.options.append(discord.SelectOption(label=task))

    @discord.ui.select(
        cls=discord.ui.Select,
        placeholder="What is your favorite fruit?",
        options=[]
    )
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_message(f"{interaction.user.mention} {select.values[0]}")
        await self.interaction.edit_original_response(content=self.interaction.message.content, view=None)


# タスクの削除するとき用のView
class MyView(discord.ui.View):
    def __init__(self, interaction):
        super().__init__()
        self.select = DynamicSelect()
        self.add_item(self.select)

    def update_select_options(self, new_options):
        self.select.set_options(new_options)


# セレクト
class DynamicSelect(Select):
    def __init__(self):
        # 初期状態では空の選択肢で初期化
        super().__init__(placeholder="選択してください", options=[])

    async def callback(self, interaction):
        await interaction.response.send_message(f"あなたが選んだのは: {self.values[0]}", ephemeral=True)

    def set_options(self, new_options):
        self.options = [SelectOption(label=opt, value=opt) for opt in new_options]


if __name__ == "__main__":
    pass
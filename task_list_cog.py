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
        self.bot: commands.Bot = bot
        self.task_repo = task_repository.TaskRepository(task_repo_file_path)
        self.gemini_service = gemini_chat_service.GeminiChatService(api_key=gemini_api_key, prompt_path=prompt_path, history_file_path=history_file_path)
        self.remind_task_list.start()
        self.guild_repo = guild_data_repository.GuildDataRepository(file_path=guild_file_path)


    # タスクリストをリマインド
    @tasks.loop(seconds=60)
    async def remind_task_list(self):
        now = datetime.datetime.now()
        #now = datetime.datetime(year=2025, month=4, day=28, hour=7, minute=0)
        for guild_data in self.guild_repo.get_data():
            if (now.hour == guild_data.h1 and now.minute == guild_data.m1) or (now.hour == guild_data.h2 and now.minute == guild_data.m2):
                self.task_repo.edit_task_path(guild_id=guild_data.guild_id)
                task_list = self.task_repo.get_all()
                if task_list == []:
                    self.gemini_service.gen_meta_data()
                    msg2 = self.gemini_service.talk(guild_id=guild_data.guild_id, system_msg=f"マスターに、簡単な挨拶、簡単な気遣いの一文、タスクがすべて終わっていることを伝える、という流れでマスターに話してください。リストの全体を表示する必要はありません。現在時刻に適した挨拶をしてください。例)おはようございます、マスター。現在取り組むべきタスクはありません。お疲れ様でした。")
                    ch = self.bot.get_channel(guild_data.ch_id)
                    try:
                        await ch.send(content=f"<@{guild_data.user_id}>\n" + msg2)
                        return
                    except:
                        print("定刻通知の送信に失敗しました") 
                msg = ""
                for task in task_list:
                    msg += f"・{task.format_to_str()}\n"
                self.gemini_service.gen_meta_data()
                msg2 = self.gemini_service.talk(guild_id=guild_data.guild_id, system_msg=f"マスターが取り組むべき「{msg}」のようなタスクがあります。簡単な挨拶、簡単な気遣いの一文、タスクについての総括、という流れでマスターに話してください。リストの全体を表示する必要はありません。現在時刻に適した挨拶をしてください。例)おはようございます、マスター。残っているタスクは集中力が必要なものが多いです。適宜休憩を挟むと良いかと思います。")
                ch = self.bot.get_channel(guild_data.ch_id)
                try:
                    await ch.send(content=f"<@{guild_data.user_id}>\n" + msg2 + "\n" + msg)
                except:
                    print("定刻通知の送信に失敗しました")

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
        options = []
        self.task_repo.edit_task_path(guild_id=interaction.guild_id)
        for task in self.task_repo.get_all():
            options.append(discord.SelectOption(label=task.name))
        self.gemini_service.gen_meta_data()
        content = self.gemini_service.talk(guild_id=interaction.guild.id, system_msg=f"マスターのあるタスクが完了したようです。どのタスクをリストから削除すればいいか尋ねてください。")
        origin_interaction = await interaction.followup.send(content = content, ephemeral = True)
        view = TaskDropdownView(placeholder="タスクを選択", origin_interaction=origin_interaction, options=options, task_repo=self.task_repo, gemini_service=self.gemini_service)
        await origin_interaction.edit(view=view)


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
        msg2 = self.gemini_service.talk(guild_id=interaction.guild_id, system_msg=f"マスターが取り組むべき「{msg}」のようなタスクがあります。簡単な挨拶、簡単な気遣いの一文、タスクについての総括、という流れでマスターに話してください。リストの全体を表示する必要はありません。現在時刻に適した挨拶をしてください。例)おはようございます、マスター。\n残っているタスクは集中力が必要なものが多いようですので、適宜休憩を挟むと良いかと思います。")
        await interaction.followup.send(content = f"<@{interaction.user.id}>\n" + msg2 + "\n" + msg, ephemeral = True)


class TaskDropdownView(discord.ui.View):
    def __init__(self, placeholder, origin_interaction, options, task_repo: task_repository.TaskRepository, gemini_service: gemini_chat_service.GeminiChatService):
        super().__init__(timeout=None)
        select = TaskSelect(placeholder=placeholder, options=options)
        select.callback = self.callback
        self.origin_message = origin_interaction
        self.add_item(select)
        self.task_repo = task_repo
        self.gemini_service = gemini_service

    async def callback(self, interaction: discord.Interaction):
        await self.origin_message.edit(view=None)
        self.task_repo.edit_task_path(interaction.guild_id)
        self.task_repo.remove(interaction.data["values"][0])
        self.gemini_service.gen_meta_data()
        content = self.gemini_service.talk(guild_id=interaction.guild.id, system_msg=f"マスターのタスクリストから「{interaction.data['values'][0]}」を削除し、その旨をマスターに伝えてください。リストの全体を表示する必要はありません。")
        await interaction.channel.send(content=content)


class TaskSelect(discord.ui.Select):
    def __init__(self, placeholder, options):
        super().__init__(options=[], placeholder=placeholder)
        for i in options:
            super().append_option(i)


if __name__ == "__main__":
    pass
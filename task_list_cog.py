import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands

from features.task_list import task_repository
import features.gemini as gemini

import re
from pathlib import Path


class TaskListCog(commands.Cog):
    # コンストラクタ
    def __init__(self, bot, task_repo_file_path):
        self.bot = bot
        self.task_repo = task_repository.TaskRepository(task_repo_file_path)


    # タスクリストをリマインド
    @tasks.loop(seconds=60)
    async def remind_task_list():
        pass


    # /add_taskコマンド
    @app_commands.describe(name="タスクの名前", date="日", time="時間")
    async def add_task_command(interaction: discord.Interaction, name: str, date:str = None, time:str = None):
        await interaction.response.defer()


    # /complete_taskコマンド
    @app_commands.describe(name="タスクの名前")
    async def remove_task_command(interaction: discord.Interaction, name: str):
        await interaction.response.defer()
    
    
    # /show_taskコマンド
    @app_commands.describe()
    async def show_task_command(interaction: discord.Interaction):
        await interaction.response.defer()
    
if __name__ == "__main__":
    task_list_cog = TaskListCog(bot="bot", task_repo_file_path=f"{Path(__file__).parent}/json/task.json")
    print(task_list_cog.task_repo.get_all())
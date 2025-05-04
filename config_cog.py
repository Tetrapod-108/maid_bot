import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
import json

from features.gemini import gemini_chat_service

import re
import datetime
from pathlib import Path


class ConfigCog(commands.Cog):
    # コンストラクタ
    def __init__(self, bot, gemini_api_key, prompt_path, history_file_path, guild_file_path):
        self.bot = bot
        self.gemini_service = gemini_chat_service.GeminiChatService(api_key=gemini_api_key, prompt_path=prompt_path, history_file_path=history_file_path)
        self.guild_file_path = guild_file_path

    # /contract_with_sekreコマンド
    @app_commands.command(name = "contract_with_sekre", description="Sekreと契約する")
    async def contract_with_sekre(self, interaction: discord.Interaction):
        await interaction.response.defer()
        with open(self.guild_file_path, "r", encoding="utf-8") as f:
            data:list = json.load(f)
        for i in data:
            if i["guild_id"] == interaction.guild.id:
                self.gemini_service.gen_meta_data()
                res = self.gemini_service.talk(guild_id=interaction.guild.id, system_msg = f"マスターのアシスタントを引き続き行ってください")
                await interaction.followup.send(content = res, ephemeral = True)
                return
        self.gemini_service.gen_meta_data()
        res = self.gemini_service.talk(guild_id=interaction.guild.id, system_msg = f"マスターと契約を行いました。このテキストチャンネルを自由に使って良いそうです。マスターに自己紹介をしてください。")
        with open(self.guild_file_path, "r", encoding="utf-8") as f:
            data:list = json.load(f)
        guild_data = {"guild_id":interaction.guild.id, "ch_id":interaction.channel.id, "user_id":interaction.user.id, "h1":7, "m1":0, "h2":21, "m2":0}
        data.append(guild_data)
        with open(self.guild_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        await interaction.followup.send(content = res, ephemeral = True)


if __name__ == "__main__":
    #task_list_cog = RemindCog(bot="bot", task_repo_file_path=f"{Path(__file__).parent}/json/task.json")
    #for task in task_list_cog.task_repo.get_all():
    #    print(task.name)
    #task_list_cog.remind_task_list()
    pass
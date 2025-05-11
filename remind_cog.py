import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands

from features.remind import remind_repository
from features.remind import remind
from features.gemini import gemini_chat_service

import re
import datetime
from pathlib import Path


class RemindCog(commands.Cog):
    # コンストラクタ
    def __init__(self, bot, remind_repo_file_path, gemini_api_key, prompt_path, history_file_path):
        self.bot: commands.Bot = bot
        self.remind_repo = remind_repository.RemindRepository(remind_repo_file_path)
        self.gemini_service = gemini_chat_service.GeminiChatService(api_key=gemini_api_key, prompt_path=prompt_path, history_file_path=history_file_path)
        self.remind_loop.start()


    # タスクリストをリマインド
    @tasks.loop(seconds=60)
    async def remind_loop(self):
        now = datetime.datetime.now()
        #now = datetime.datetime(year=2025, month=4, day=28, hour=21, minute=0)
        remind_list = self.remind_repo.search(date=now)
        if remind_list != []:
            for i in remind_list:
                ch = self.bot.get_channel(int(i.ch_id))
                await ch.send(content=f"<@{i.user}>\n {i.name}")
                self.remind_repo.remove(i)

    @remind_loop.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()


    # /add_remindコマンド
    @app_commands.command(name = "add_remind", description="リマインドを追加する")
    @app_commands.describe(time="リマインドする時間 例) 1d2h3m、13:00", msg="リマインドしたいメッセージ")
    async def add_remind(self, interaction: discord.Interaction, time: str, msg: str):
        await interaction.response.defer()
        now = datetime.datetime.now()
        rmd = remind.Remind(name=msg, date=now, user=str(interaction.user.id), ch_id=str(interaction.channel_id))
        try:
            rmd.edit_date(in_date=time)
            self.remind_repo.add(rmd)
            self.gemini_service.gen_meta_data()
            res = self.gemini_service.talk(guild_id=interaction.guild.id, system_msg = f"マスターに、{time}に「{msg}」と通知してください。現在時刻からの相対時間で時間を伝えてください。")
        except:
            self.gemini_service.gen_meta_data()
            res = self.gemini_service.talk(guild_id=interaction.guild.id, system_msg = f"マスターから受けた指示が間違っていることを伝えてください。")
        await interaction.followup.send(content = res, ephemeral = True)
 

if __name__ == "__main__":
    #task_list_cog = RemindCog(bot="bot", task_repo_file_path=f"{Path(__file__).parent}/json/task.json")
    #for task in task_list_cog.task_repo.get_all():
    #    print(task.name)
    #task_list_cog.remind_task_list()
    pass
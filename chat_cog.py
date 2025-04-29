import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands

from features.gemini import gemini_chat_service

import re
import datetime
from pathlib import Path


class ChatCog(commands.Cog):
    # コンストラクタ
    def __init__(self, bot, gemini_api_key, prompt_path, history_file_path):
        self.bot = bot
        self.gemini_service = gemini_chat_service.GeminiChatService(api_key=gemini_api_key, prompt_path=prompt_path, history_file_path=history_file_path)


    # チャットに反応
    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author == self.bot.user:
            return
        if msg.channel.id != 1319690391251062835:
            return

        # チャットに反応
        self.gemini_service.gen_meta_data()
        res = self.gemini_service.talk(guild_id=msg.guild.id, msg=msg.content)
        await msg.reply(content = res)


"""
    @self.bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            # コマンドが見つからないエラーを無視
            return
        # 他のエラーは再度発生させる
        raise error
"""
        
if __name__ == "__main__":
    pass
import discord
from discord import app_commands
from discord.ext import tasks
from discord.ext import commands
from pathlib import Path

import task_list_cog
import remind_cog
import chat_cog

import key


# 各種変数
GUILD_ID = 748871577377964054
TASK_FILE_PATH = f"{Path(__file__).parent}/json/task.json"
REMIND_FILE_PATH = f"{Path(__file__).parent}/json/remind.json"
HISTORY_FILE_PATH = f"{Path(__file__).parent}/json/history.json"
PROMPT_PATH = f"{Path(__file__).parent}/json/system_prompt_new.json"
GEMINI_API_KEY = key.GEMINI_API_KEY
DISCORD_BOT_TOKEN = key.DISCORD_BOT_TOKEN


# botをインスタンス化
bot = commands.Bot(command_prefix="", intents=discord.Intents.all())
tree = bot.tree

# botの準備完了時にメッセージ 
@bot.event
async def on_ready():
    
    # 各種コグを追加
    await bot.add_cog(task_list_cog.TaskListCog(
        bot=bot,
        task_repo_file_path=TASK_FILE_PATH,
        gemini_api_key=GEMINI_API_KEY,
        prompt_path=PROMPT_PATH,
        history_file_path=HISTORY_FILE_PATH
        ),
        guild=discord.Object(GUILD_ID)
    )
    await bot.add_cog(remind_cog.RemindCog(
        bot=bot,
        remind_repo_file_path=REMIND_FILE_PATH,
        gemini_api_key=GEMINI_API_KEY,
        prompt_path=PROMPT_PATH,
        history_file_path=HISTORY_FILE_PATH
        ),
        guild=discord.Object(GUILD_ID)    
    )
    await bot.add_cog(chat_cog.ChatCog(
        bot=bot,
        gemini_api_key=GEMINI_API_KEY,
        prompt_path=PROMPT_PATH,
        history_file_path=HISTORY_FILE_PATH
        ),
        guild=discord.Object(GUILD_ID)
    )

    #tree.clear_commands(guild=discord.Object(GUILD_ID))
    await tree.sync(guild=discord.Object(GUILD_ID))
    print(bot.user.name + " is ready!")
   

# tokenを読み込んでbotを起動
bot.run(DISCORD_BOT_TOKEN)
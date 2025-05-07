import discord
from discord import app_commands
from discord.ext import tasks
from discord.ext import commands
from pathlib import Path
import json

import task_list_cog
import remind_cog
import chat_cog
import config_cog
import test_cog

import config.key as key


# 各種変数
TASK_FILE_PATH = f"{Path(__file__).parent/'data'/'XXX'/'task.json'}"
REMIND_FILE_PATH = f"{Path(__file__).parent/'json'/'remind.json'}"
HISTORY_FILE_PATH = f"{Path(__file__).parent/'data'/'XXX'/'history.json'}"
#PROMPT_PATH = f"{Path(__file__).parent}/json/system_prompt_new.json"
PROMPT_PATH = f"{Path(__file__).parent/'config'/'prompt.md'}"
GUILD_FILE_PATH = f"{Path(__file__).parent/'json'/'guild_data.json'}"
GEMINI_API_KEY = key.GEMINI_API_KEY
DISCORD_BOT_TOKEN = key.DISCORD_BOT_TOKEN


# botをインスタンス化
intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.guild_reactions = True
intents.emojis = True
intents.members = True
bot = commands.Bot(command_prefix="", intents=intents)
tree = bot.tree

# botの準備完了時に実行
@bot.event
async def on_ready():
    # 各種コグを追加
    await bot.add_cog(task_list_cog.TaskListCog(
        bot=bot,
        task_repo_file_path=TASK_FILE_PATH,
        gemini_api_key=GEMINI_API_KEY,
        prompt_path=PROMPT_PATH,
        history_file_path=HISTORY_FILE_PATH,
        guild_file_path=GUILD_FILE_PATH
        ),
        guilds=bot.guilds
    )
    await bot.add_cog(remind_cog.RemindCog(
        bot=bot,
        remind_repo_file_path=REMIND_FILE_PATH,
        gemini_api_key=GEMINI_API_KEY,
        prompt_path=PROMPT_PATH,
        history_file_path=HISTORY_FILE_PATH
        ),
        guilds=bot.guilds  
    )
    await bot.add_cog(chat_cog.ChatCog(
        bot=bot,
        gemini_api_key=GEMINI_API_KEY,
        prompt_path=PROMPT_PATH,
        history_file_path=HISTORY_FILE_PATH
        ),
        guilds=bot.guilds
    )
    await bot.add_cog(config_cog.ConfigCog(
        bot=bot,
        gemini_api_key=GEMINI_API_KEY,
        prompt_path=PROMPT_PATH,
        history_file_path=HISTORY_FILE_PATH,
        guild_file_path=GUILD_FILE_PATH
        ),
        guilds=bot.guilds
    )
    await bot.add_cog(test_cog.TestCog(
        bot=bot
        ),
        guilds=bot.guilds
    )

    #tree.clear_commands(guild=discord.Object(GUILD_ID))
    guilds = bot.guilds
    for guild in guilds:
        await tree.sync(guild=guild)
    print(bot.user.name + " is ready!")


# サーバー加入時にディレクトリとファイルを生成
@bot.event
async def on_guild_join(guild):
    path = Path(f"{Path(__file__).parent}/data/{guild.id}")
    path.mkdir(parents=True, exist_ok=True)
    with open(f"{path/'histoy.json'}", "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)
    with open(f"{path/'task.json'}", "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)


class SampleView(discord.ui.View):
    def __init__(self, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.select(
        cls=discord.ui.Select,
        placeholder="What is your favorite fruit?",
        options=[
            discord.SelectOption(label="Banana"),
            discord.SelectOption(label="Apple"),
            discord.SelectOption(label="Pineapple"),
            discord.SelectOption(label="Grapefruit"),
            discord.SelectOption(label="Orange"),
        ]
    )
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_message(f"{interaction.user.mention} {select.values[0]}")
        

# tokenを読み込んでbotを起動
bot.run(DISCORD_BOT_TOKEN)
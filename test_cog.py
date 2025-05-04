import discord

import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands


class TestCog(commands.Cog):
    # コンストラクタ
    def __init__(self, bot):
        self.bot = bot


    # /testコマンド
    @app_commands.command(name = "test", description="テスト用")
    async def add_remind(self, interaction: discord.Interaction):
        await interaction.response.defer()
        view = TaskView(timeout=20, interaction=interaction)
        await interaction.followup.send(view=view, ephemeral = True)
        #await interaction.edit_original_response(content="完了しました。", view=None)


class TaskView(discord.ui.View):
    def __init__(self, timeout, interaction: discord.Interaction):
        super().__init__(timeout=timeout)
        self.interaction = interaction

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
        await self.interaction.edit_original_response(content=self.interaction.message.content, view=None)
import discord

import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands


class TestCog(commands.Cog):
    # コンストラクタ
    def __init__(self, bot):
        self.bot: commands.Bot = bot


    # /testコマンド
    @app_commands.command(name = "test", description="テスト用")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.defer()
        options=[
            discord.SelectOption(label="1"),
            discord.SelectOption(label="2"),
            discord.SelectOption(label="3")
        ]
        await interaction.followup.send(content="ああ", ephemeral=True)
        ch = self.bot.get_channel(1319690391251062835)
        msg: discord.Message = await ch.send(content="ff")
        options=[
            discord.SelectOption(label="1"),
            discord.SelectOption(label="2"),
            discord.SelectOption(label="3")
        ]
        view = TaskDropdownView(placeholder="削除するタスクを選んでください", origin_message=msg, options=options)
        await msg.edit(view=view)
        #await interaction.edit_original_response(content="完了しました。", view=None)


class TaskDropdownView(discord.ui.View):
    def __init__(self, placeholder, origin_message: discord.Message, options):
        super().__init__(timeout=None)
        select = TaskSelect(placeholder=placeholder, options=options)
        select.callback = self.callback
        self.origin_message = origin_message
        self.add_item(select)

    async def callback(self, interaction: discord.Interaction):
        await self.origin_message.delete()
        await interaction.channel.send(f"あなたが選んだ選択肢は{interaction.data["values"][0]}です。")
        #await self.origin_message.edit(content=self.origin_message.content, view=None)


class TaskSelect(discord.ui.Select):
    def __init__(self, placeholder, options):
        super().__init__(options=[], placeholder=placeholder)
        for i in options:
            super().append_option(i)
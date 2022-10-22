import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import Bot, Context
from disnake.ext.commands.cog import Cog

from bot import constants

from bot.utils.with_role import with_role


class ExerciseManager(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @tasks.loop(seconds=60)
    async def monitor_submissions(self):
        pass


def setup(bot: Bot):
    bot.add_cog(ExerciseManager(bot))

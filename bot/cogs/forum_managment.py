import disnake
from disnake.ext import commands
from disnake.ext.commands import Bot, Context
from disnake.ext.commands.cog import Cog
import disnake.ext.tasks as tasks

import arrow

from bot import constants

from bot.utils.with_role import with_role
from bot.utils.auto_close_exercise import set_duration, get_duration


class ForumManager(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.auto_close.start()

    @with_role(constants.Roles.admin, constants.Roles.manager)
    @commands.slash_command(name="open-exercise")
    async def open_exercise(
        self,
        inter: disnake.ApplicationCommandInteraction,
        exercise_no: int,
        duration: int = 5,
    ):

        forum_channel: disnake.ForumChannel = self.bot.get_channel(
            constants.Channels.weekly_exercise_forum
        )

        open_exercises = [
            tag.name
            for tag in forum_channel.available_tags
            if tag.name.startswith("open")
        ]

        exercise_already_exists = (
            len(
                [
                    tag
                    for tag in forum_channel.available_tags
                    if str(exercise_no) in tag.name
                ]
            )
            > 0
        )

        if len(open_exercises) > 0:
            await inter.response.send_message(
                content=f"Below exercise are open, close them before opening a new one.\n**{' | '.join(open_exercises)}**"
            )
            return

        elif exercise_already_exists:
            await inter.response.send_message(
                content=f"Use a different exercise number, Exercise {exercise_no} was already claimed."
            )
            return

        else:
            tag = disnake.ForumTag(name=f"open[wk-{exercise_no}]")
            avlbl_tags = forum_channel.available_tags
            avlbl_tags.append(tag)

            await forum_channel.edit(available_tags=avlbl_tags)
            await set_duration(days=duration, exercise_no=exercise_no)
            await inter.response.send_message(
                content=f"Exercise {exercise_no} is open now!"
            )

            await self.exercise_notification_embed(exercise_no=exercise_no, close=False)
            return

    @with_role(constants.Roles.admin, constants.Roles.manager)
    @commands.slash_command(name="close-exercise")
    async def close_exercise(
        self, inter: disnake.ApplicationCommandInteraction, exercise_no: int
    ):

        await self._close_exercise(inter=inter, exercise_no=exercise_no)

    @tasks.loop(hours=3)
    async def auto_close(self):
        dur, ex_no = await get_duration()

        if (arrow.now().timestamp() - dur.timestamp()) >= 0:
            await self._close_exercise(exercise_no=ex_no)

    @auto_close.before_loop
    async def before_auto_close_begin(self):
        await self.bot.wait_until_ready()

    async def _close_exercise(
        self, exercise_no: int, inter: disnake.ApplicationCommandInteraction = None
    ):

        forum_channel: disnake.ForumChannel = self.bot.get_channel(
            constants.Channels.weekly_exercise_forum
        )

        open_exercises_names = [
            tag.name
            for tag in forum_channel.available_tags
            if tag.name.startswith("open")
        ]

        if f"open[wk-{exercise_no}]" in open_exercises_names:
            if inter:
                await inter.send(content=f"Closed **wk-{exercise_no}** exercise")
                await self.exercise_notification_embed(
                    exercise_no=exercise_no, close=True
                )
        else:
            if inter:
                await inter.send(
                    content=f"No open exercise with exercise number {exercise_no}"
                )
            return

        avlbl_tags = forum_channel.available_tags
        for i in range(len(avlbl_tags)):
            if avlbl_tags[i].name == f"open[wk-{exercise_no}]":
                _tmp = avlbl_tags[i]
                _tmp.name = f"closed[wk-{exercise_no}]"
                _tmp.moderated = True
                avlbl_tags[i] = _tmp.with_changes()

                await forum_channel.edit(available_tags=avlbl_tags)

                await set_duration(revoke=True)
                break

    async def exercise_notification_embed(self, exercise_no: int, close: bool = False):
        if close:
            title = f"Ex - {exercise_no}, has been closed!"
        else:
            title = f"Ex - {exercise_no}, is now open!"

        await self.bot.get_channel(constants.Channels.exercise_noti).send(
            embed=disnake.Embed(
                title=title,
                color=constants.Color.primary,
                url=self.bot.get_channel(
                    constants.Channels.weekly_exercise_forum
                ).jump_url,
            )
        )


def setup(bot: Bot):
    bot.add_cog(ForumManager(bot))

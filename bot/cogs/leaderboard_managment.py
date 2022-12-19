import disnake
import asyncio
from disnake.ext import commands
from disnake.ext.commands import Bot, Context
from disnake.ext.commands.cog import Cog
import disnake.ext.tasks as tasks

import arrow

from bot import constants

from bot.utils.with_role import with_role
from bot.utils.auto_close_exercise import set_duration, get_duration


class LeaderboardManager(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.exercise_no = None
        self.webhook = None
        self.leaderboard_message = None

    @with_role(constants.Roles.admin, constants.Roles.manager)
    @commands.slash_command(name="watch")
    async def watch_leaderboard_cmd(
        self,
        inter: disnake.ApplicationCommandInteraction,
        exercise_no: int,
    ):

        forum_channel: disnake.ForumChannel = self.bot.get_channel(
            constants.Channels.weekly_exercise_forum
        )

        open_exercises = [
            tag.name
            for tag in forum_channel.available_tags
            if tag.name.startswith("open")
        ]

        if len(open_exercises) == 0:
            await inter.send("No open exercises to watch")
            return

        exercise_exists = (
            len(
                [
                    exercise
                    for exercise in open_exercises
                    if str(exercise_no) in exercise
                ]
            )
            == 1
        )

        if not exercise_exists:
            await inter.send(f"No open exercise with, exercise no: {exercise_no}")
            return

        self.exercise_no = exercise_no

        self.watch_leaderboard.start()

        await inter.send(content=f"Watching Ex - {exercise_no}")

    @with_role(constants.Roles.admin, constants.Roles.manager)
    @commands.slash_command(name="unwatch")
    async def unwatch_leaderboard_cmd(
        self,
        inter: disnake.ApplicationCommandInteraction,
        exercise_no: int,
    ):

        if self.exercise_no != exercise_no:
            await inter.send(content=f"Ex - {exercise_no} is not on the watch queue.")
            return

        if self.exercise_no is None:
            await inter.send(content="No current exercises on watch queue.")
            return

        self.watch_leaderboard.stop()

        await inter.send(content=f"Stopped watching Ex-{self.exercise_no}")

        self.exercise_no = None
        self.leaderboard_message = None

    @tasks.loop(seconds=30 * 60)
    async def watch_leaderboard(self):

        forum_channel: disnake.ForumChannel = self.bot.get_channel(
            constants.Channels.weekly_exercise_forum
        )

        submissions = [
            submission
            for submission in forum_channel.threads
            if f"open[wk-{self.exercise_no}]"
            in [tag.name for tag in submission.applied_tags]
        ]

        post_messages = [
            await submission.fetch_message(submission.id) for submission in submissions
        ]

        post_data = {}

        for post in post_messages:
            reaction_count = [
                reaction.count for reaction in post.reactions if reaction.emoji == "⬆️"
            ]
            pins = await post.channel.pins()

            if pins is not None:
                pin = pins[0]
            if len(reaction_count) != 0:
                reaction_count = reaction_count[0]
            else:
                reaction_count = 0

            post_data[post.id] = {
                "upvotes": int(reaction_count),
                "jump_url": pin.jump_url,
                "display_name": post.author.display_name,
            }

        leaderboard = []

        posts = [key for key in post_data.keys()]

        # sort posts  according to upvotes

        if len(posts) > 1:
            leaderboard = [
                x[1]
                for x in list(
                    sorted(
                        post_data.items(),
                        key=lambda kv: kv[1].get("upvotes"),
                        reverse=True,
                    )
                )
            ]

        embed = await self.create_leaderboard_embed(leaderboard_data=leaderboard)
        await self.webhook.edit_message(self.leaderboard_message.id, embed=embed)

    async def create_leaderboard_embed(self, leaderboard_data=[]):

        embed = disnake.Embed(
            title=f"Exercise - {self.exercise_no} Leaderboard",
            color=constants.Color.primary,
            url=self.bot.get_channel(constants.Channels.weekly_exercise_forum).jump_url,
        )

        embed.set_footer(text="Updated every 30 minutes")

        board = ""
        for rank in leaderboard_data:
            board += f"\n❯ ⬆️ [{str(rank['upvotes'])}] - [{str(rank['display_name'])}]({rank['jump_url']})"
        embed.description = board

        return embed

    @watch_leaderboard.before_loop
    async def initiate_webhook_message(self):

        leader_board_channel: disnake.TextChannel = self.bot.get_channel(
            constants.Channels.leaderboard_noti
        )

        forum_channel: disnake.ForumChannel = self.bot.get_channel(
            constants.Channels.weekly_exercise_forum
        )

        webhook = [
            hook
            for hook in await leader_board_channel.webhooks()
            if hook.id == constants.Webhooks.leaderboard
        ][0]

        self.webhook = webhook
        self.leaderboard_message = await self.webhook.send(
            wait=True, content="Leaderboard"
        )


def setup(bot: Bot):
    bot.add_cog(LeaderboardManager(bot=bot))

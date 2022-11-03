from typing import List
from uuid import uuid4

import disnake
from bot import constants
from bot.utils.with_role import with_role
from disnake.ext import commands, tasks
from disnake.ext.commands import Bot, Context
from disnake.ext.commands.cog import Cog


class ExerciseManager(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.prev_threads: List[disnake.Thread] = []
        self.submissions_to_pin = dict()

        self.monitor_submissions.start()
        self.pin_submissions.start()

    @tasks.loop(seconds=5)
    async def monitor_submissions(self):
        forum_channel: disnake.ForumChannel = self.bot.get_channel(
            constants.Channels.weekly_exercise_forum
        )

        curr_threads = forum_channel.threads

        prev_thread_ids = [thread.id for thread in self.prev_threads]

        new_threads = []

        for thread in curr_threads:
            if thread.id not in prev_thread_ids:
                new_threads.append(forum_channel.get_thread(thread.id))

        self.prev_threads = forum_channel.threads

        for thread in new_threads:
            week_tags = [
                tag.name for tag in thread.applied_tags if tag.name.startswith("open[")
            ]

            if len(week_tags) == 1:
                await self.register_new_submission(thread.id)

    @tasks.loop(seconds=10)
    async def pin_submissions(self):

        forum_channel: disnake.ForumChannel = self.bot.get_channel(
            constants.Channels.weekly_exercise_forum
        )

        has_pinned = []
        for key in self.submissions_to_pin.keys():
            submission = self.submissions_to_pin.get(key)

            sub_thread = forum_channel.get_thread(submission.get("thread"))

            lst_msg = sub_thread.last_message
            if lst_msg.author.id == sub_thread.owner.id:
                if len(lst_msg.attachments) > 0:
                    types = [atch.content_type for atch in lst_msg.attachments]
                    if "application/pdf" in types:
                        await lst_msg.pin(reason="Submission pdf")
                await sub_thread.send(content="Submission pinned.")
                has_pinned.append(key)

        for key in has_pinned:
            self.submissions_to_pin.pop(key)

    @pin_submissions.before_loop
    @monitor_submissions.before_loop
    async def before_begin(self):
        await self.bot.wait_until_ready()

    async def register_new_submission(self, thread_id):

        forum_channel: disnake.ForumChannel = self.bot.get_channel(
            constants.Channels.weekly_exercise_forum
        )

        thread = forum_channel.get_thread(thread_id)

        msg: disnake.Message = await thread.send(
            content="Upload the pdf right after this message. Make sure you wait till you recieve a **Submission pinned** message."
        )

        self.submissions_to_pin[str(uuid4())[:4]] = {"thread": thread.id, "msg": msg.id}


def setup(bot: Bot):
    bot.add_cog(ExerciseManager(bot))

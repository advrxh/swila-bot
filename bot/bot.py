import socket
import random
from typing import Optional

import disnake
from aiohttp import AsyncResolver, ClientSession, TCPConnector
from disnake.ext import commands
from loguru import logger

from bot import constants
from bot.utils.help import BotHelp


class SwilaBot(commands.Bot):
    """Base bot instance."""

    name = "Swila"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            help_command=BotHelp(),
        )

        self.http_session: Optional[ClientSession] = None
        self._connector: Optional[TCPConnector] = None

    async def login(self, *args, **kwargs) -> None:
        """Re-create the connector and set up sessions before logging into Discord."""
        # Use asyncio for DNS resolution instead of threads so threads aren't spammed.
        self._connector = TCPConnector(
            resolver=AsyncResolver(),
            family=socket.AF_INET,
        )

        # super() will use this connection for it's internal session.
        self.http.connector = self._connector

        self.http_session = ClientSession(connector=self._connector)

        await super().login(*args, **kwargs)

    async def close(self) -> None:
        """Close http session when bot is shutting down."""
        await super().close()

        if self.http_session:
            await self.http_session.close()
        if self._connector:
            await self._connector.close()

    async def on_ready(self) -> None:
        await self.check_channels()

    def add_cog(self, cog: commands.Cog) -> None:
        """
        Delegate to super to register `cog`.

        This only serves to make the info log, so that extensions don't have to.
        """
        super().add_cog(cog)
        logger.info("Cog loaded: {}", cog.qualified_name)

    async def check_channels(self) -> None:
        """Verifies that all channel constants refer to channels which exist."""
        if constants.Bot.debug:
            logger.info("Skipping Channels Check.")
            return

        all_channels_ids = {channel.id for channel in self.get_all_channels()}
        for name, channel_id in vars(constants.Channels).items():
            if name.startswith("_"):
                continue
            if channel_id not in all_channels_ids:
                logger.error('Channel "{}" with ID {} missing', name, channel_id)
    async def on_member_join(self, member: disnake.Member):
        
        guild : disnake.Guild = self.get_guild(constants.Bot.guild)

        await guild.get_channel(constants.Channels.welcome_channel).send(f"Hey {member.mention}! welcome to Swila.\n{random.choice(constants.Responses.WELCOME)}")
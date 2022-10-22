from typing import Callable

import disnake
from disnake.ext import commands
from disnake.ext.commands import Context
from loguru import logger


def with_role(*role_ids: int) -> Callable:
    """Returns True if the user has any one of the roles in role_ids."""

    async def predicate(
        context: Context = None, inter: disnake.ApplicationCommandInteraction = None
    ) -> bool:
        """With role checker predicate."""
        ctx = context or inter

        if isinstance(ctx, Context):
            cmd = ctx.command.name

        elif isinstance(ctx, disnake.ApplicationCommandInteraction):
            cmd = ctx.application_command.name

        if not ctx.guild:  # Return False in a DM
            logger.debug(
                "{} tried to use the '{}'command from a DM. "
                "This command is restricted by the with_role decorator. Rejecting request.",
                ctx.author,
                cmd,
            )
            return False

        for role in ctx.author.roles:
            if role.id in role_ids:
                logger.debug(
                    "{} has the '{}' role, and passes the check.", ctx.author, role.name
                )
                return True

        logger.debug(
            "{} does not have the required role to use the '{}' command, so the request is rejected.",
            ctx.author,
            cmd,
        )

        await ctx.send(
            "You don't have the required role permissions to use this command."
        )
        return False

    return commands.check(predicate)

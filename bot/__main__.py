import disnake
from disnake.ext.commands import when_mentioned_or
from loguru import logger

from bot import bot, constants
from bot.utils.exceptions import MissingToken

# Set the required Intents to True
intents = disnake.Intents.all()
intents.presences = False

# Initialize the bot
bot = bot.SwilaBot(
    command_prefix=when_mentioned_or(
        constants.Bot.prefix
    ),  # Invoked commands must have this prefix
    activity=disnake.Streaming(
        platform="Swila",
        details="Managing the Swila Discord Forum",
        name="ABW | Always be Writing",
        url="https://screenwritinginla.com",
    ),
    case_insensitive=True,
    allowed_mentions=disnake.AllowedMentions(everyone=True, roles=True),
    intents=intents,
)

# Load the extensions we want

# Validate the token
token = constants.Bot.token

if token is None:
    raise MissingToken(
        "No token found in the SWILA_DISCORD_TOKEN environment variable!"
    )

# Start the bot
logger.info("SWILA BOT OPERATIONAL 🎥")
bot.run(token)

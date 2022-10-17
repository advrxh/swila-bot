import os
from pathlib import Path
from typing import Optional

POSITIVE_VERBS = ["pronounces", "decrees", "proclaims", "ordains"]
NEGATIVE_VERBS = ["commands", "orders", "demands", "dictates"]
UNCERTAIN_VERBS = ["mumbles", "suggests", "mutters", "shrugs, and says"]

NEGATIVE_REPLIES = [
    "Noooooo!!",
    "Nope.",
    "I don't think so.",
    "Not gonna happen.",
    "Out of the question.",
    "Huh? No.",
    "Nah.",
    "Naw.",
    "Not likely.",
    "No way, José.",
    "Not in a million years.",
    "Fat chance.",
    "Certainly not.",
    "NEGATORY.",
    "Nuh-uh.",
    "Not in my house!",
]

POSITIVE_REPLIES = [
    "Yep.",
    "Absolutely!",
    "Can do!",
    "Affirmative!",
    "Yeah okay.",
    "Sure.",
    "Sure thing!",
    "You're the boss!",
    "Okay.",
    "No problem.",
    "I got you.",
    "Alright.",
    "You got it!",
    "ROGER THAT",
    "Of course!",
    "Aye aye, cap'n!",
    "I'll allow it.",
]

UNCERTAIN_REPLIES = [
    "I have no idea.",
    "How would I know?",
    "Ask me tomorrow.",
    "Ask me when you're older.",
    "Maybe?",
    "It's hard to say for sure.",
    "Who knows?",
    "Nyesno.",
    "Sure! Wait, maybe not.",
    "You never know!",
    "I know the answer, but I won't tell you.",
    "Frudgeknuckle.",
    "Rorchestershire.",
    "Could go either way!",
]

ERROR_REPLIES = [
    "Please don't do that.",
    "You have to stop.",
    "Do you mind?",
    "In the future, don't do that.",
    "That was a mistake.",
    "You blew it.",
    "You're bad at computers.",
    "Are you trying to kill me?",
    "Noooooo!!",
    "I can't believe you've done this",
]


class Bot:
    """Constants relating to the bot itself."""

    token: Optional[str] = os.environ.get("SWILA_DISCORD_TOKEN")
    prefix: str = "."
    debug: bool = os.environ.get("SWILA_DEBUG", "false").lower() == "true"
    guild: int = 1007505851357073509


class Color:
    """Constant containing color values."""

    yellow: int = 0xF6F65D


class Channels:
    """Channel IDs that are relevant for this community."""

    pass


class Messages:
    """Message IDs that are important."""

    pass


class Roles:
    """Roles relevant to this bot."""

    pass


class Users:
    """Users relevant to this bot."""

    pass

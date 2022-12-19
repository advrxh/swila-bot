import os
from pathlib import Path
from typing import Optional


_debug = os.environ.get("SWILA_DEBUG", "false").lower() == "true"

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

    if debug:
        guild: int = 1031589477983989812
    else:
        guild: int = 1007505851357073509


class Color:
    """Constant containing color values."""

    primary: int = 0x082612


class Channels:
    """Channel IDs that are relevant for this community."""

    if _debug:
        welcome_channel = 1033291440329064448
        weekly_exercise_forum = 1033287983463399454
        exercise_noti = 1033393548365680660
        leaderboard_noti = 1040869766853828650


class Messages:
    """Message IDs that are important."""

    pass


class Roles:
    """Roles relevant to this bot."""

    if _debug:
        admin = 1033289362219208825
        manager = 1033289362219208825


class Users:
    """Users relevant to this bot."""

    pass


class Webhooks:
    """webhooks relevant to the bot."""

    if _debug:
        leaderboard = 1040869801758822425


class Responses:
    """Responses relevant to the bot"""

    WELCOME = [
        "We're happy to have you here!",
        "We're excited to see you around.",
        "Always be writing!",
    ]


class Paths:
    """File/Folder paths relevant to the bot"""

    DATA_STORE = Path(os.environ.get("ROOT_DIR") + "deps/data_store.json")

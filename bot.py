"""Discord bot that removes messages older than the configured retention period."""

from __future__ import annotations

import asyncio
import datetime as dt
import logging
import os
import random

import discord
from discord.ext import commands, tasks

LOG = logging.getLogger("discord-autodelete")
RETENTION_DAYS = 7

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


def utcnow() -> dt.datetime:
    """Return an aware UTC timestamp compatible with discord.py 2.x."""

    return dt.datetime.now(dt.UTC)


async def delete_old_messages_in_channel(channel: discord.TextChannel) -> int:
    """Delete non-bot messages older than the retention period from one channel."""

    deleted = 0
    cutoff = utcnow() - dt.timedelta(days=RETENTION_DAYS)
    LOG.info("fetching expired messages", extra={"channel_id": channel.id})

    try:
        async for message in channel.history(limit=None, before=cutoff):
            if message.author == bot.user:
                continue

            await message.delete()
            deleted += 1
            # Message content and author details are intentionally not logged.
            LOG.info(
                "deleted expired message",
                extra={"channel_id": channel.id, "message_id": message.id},
            )
            await asyncio.sleep(1)
    except discord.Forbidden:
        LOG.warning("missing permission to delete messages", extra={"channel_id": channel.id})
    except discord.HTTPException:
        LOG.exception("Discord API error while deleting messages", extra={"channel_id": channel.id})

    return deleted


@tasks.loop(minutes=5)
async def delete_old_messages() -> None:
    """Process text channels in randomized order to avoid persistent starvation."""

    channels = list(bot.get_all_channels())
    random.SystemRandom().shuffle(channels)
    for channel in channels:
        if isinstance(channel, discord.TextChannel):
            await delete_old_messages_in_channel(channel)


@delete_old_messages.before_loop
async def before_delete_loop() -> None:
    await bot.wait_until_ready()


@bot.event
async def on_ready() -> None:
    LOG.info("bot connected", extra={"bot_user_id": getattr(bot.user, "id", None)})
    if not delete_old_messages.is_running():
        delete_old_messages.start()


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise SystemExit("DISCORD_TOKEN is required")
    bot.run(token, log_handler=None)


if __name__ == "__main__":
    main()

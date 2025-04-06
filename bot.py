import discord
from discord.ext import commands, tasks
import os
import datetime
import asyncio
import sys  
import random

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!")

last_execution_time = None

@tasks.loop(minutes=1)
async def delete_old_messages():
    global last_execution_time
    current_time = datetime.datetime.utcnow()
    print(f"{datetime.datetime.now()} - Looping...")
    sys.stdout.flush()  

    if last_execution_time is None or (current_time - last_execution_time).total_seconds() >= 300:
        last_execution_time = current_time
        print(f"{datetime.datetime.now()} - Starting deletion of old messages...")
        sys.stdout.flush()
        channels = list(bot.get_all_channels())
        random.shuffle(channels)  # Shuffle the list of channels
        for channel in channels:
            if isinstance(channel, discord.TextChannel):
                await delete_old_messages_in_channel(channel)

async def delete_old_messages_in_channel(channel):
    print(f"{datetime.datetime.now()} - Fetching messages from channel: {channel.name}")
    sys.stdout.flush()  
    try:
        current_time = datetime.datetime.utcnow()
        async for message in channel.history(limit=None, before=current_time - datetime.timedelta(days=7)):
            if message.author == bot.user:
                continue

            await message.delete()
            print(f"{datetime.datetime.now()} - Deleted message (created at: {message.created_at}) from {message.author} in {channel.name}: {message.content} (older than 7 days)")
            sys.stdout.flush()  
            await asyncio.sleep(1)
    except discord.errors.Forbidden:
        print(f"{datetime.datetime.now()} - Error: Bot does not have permission to delete messages in channel {channel.name}")
        sys.stdout.flush()  
    except Exception as e:
        print(f"{datetime.datetime.now()} - An error occurred while deleting messages in channel {channel.name}: {e}")
        sys.stdout.flush()  
    print(f"{datetime.datetime.now()} - Finished processing messages in channel: {channel.name}")
    sys.stdout.flush()  

@bot.event
async def on_ready():
    print(f"{datetime.datetime.now()} - Logged in as {bot.user}")
    print(f"{datetime.datetime.now()} - Bot is ready to delete old messages.")
    print(f"{datetime.datetime.now()} - ------")
    sys.stdout.flush()  
    delete_old_messages.start()
    print(f"{datetime.datetime.now()} - Bot is now running deletion task.")
    sys.stdout.flush()  

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"{datetime.datetime.now()} - An error occurred in event {event}: {args[0]}")
    sys.stdout.flush()  

@bot.event
async def on_command_error(ctx, error):
    print(f"{datetime.datetime.now()} - An error occurred in command '{ctx.command}': {error}")
    sys.stdout.flush()  

bot.run(DISCORD_TOKEN)

# bot.py

import os
import json
import requests
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables from a .env file
load_dotenv()

STEAM_API_KEY = os.getenv('STEAM_API_KEY')
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
STEAM_USER_IDS = os.getenv('STEAM_USER_IDS').split(',')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger(__name__)

TRADE_LINK_FILE = 'trade_links.json'

# Initialize the bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

def save_trade_links(links):
    with open(TRADE_LINK_FILE, 'w') as f:
        json.dump(links, f)

def load_trade_links():
    if os.path.exists(TRADE_LINK_FILE):
        with open(TRADE_LINK_FILE, 'r') as f:
            return json.load(f)
    return {}

# Function to change Steam trade link
def change_trade_link(user_id):
    try:
        # Placeholder for actual Steam API call to change the trade link
        new_trade_link = f"https://steamcommunity.com/tradeoffer/new/?partner={user_id}&token=new_token_{user_id}"
        trade_links = load_trade_links()
        trade_links[user_id] = new_trade_link
        save_trade_links(trade_links)
        logger.info(f"Trade link for user {user_id} changed to: {new_trade_link}")
        return new_trade_link
    except Exception as e:
        logger.error(f"Failed to change trade link for user {user_id}: {e}")
        return None

# Task to send the new trade links via Discord
@tasks.loop(days=14)
async def update_trade_links():
    for user_id in STEAM_USER_IDS:
        new_trade_link = change_trade_link(user_id)
        if new_trade_link:
            channel = bot.get_channel(DISCORD_CHANNEL_ID)
            if channel:
                await channel.send(f"New Steam trade link for user {user_id}: {new_trade_link}")
            else:
                logger.error(f"Channel with ID {DISCORD_CHANNEL_ID} not found.")
        else:
            logger.error(f"Failed to obtain new trade link for user {user_id}.")

# Command to manually update the trade link for a specific user
@bot.command(name='update_trade_link')
async def manual_update_trade_link(ctx, user_id: str):
    if user_id in STEAM_USER_IDS:
        new_trade_link = change_trade_link(user_id)
        if new_trade_link:
            await ctx.send(f"New Steam trade link for user {user_id}: {new_trade_link}")
        else:
            await ctx.send(f"Failed to update trade link for user {user_id}.")
    else:
        await ctx.send(f"User ID {user_id} is not recognized.")

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="Managing Trade Links"))
    update_trade_links.start()
    # Send the current trade links on start
    current_trade_links = load_trade_links()
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        for user_id, trade_link in current_trade_links.items():
            await channel.send(f"Current Steam trade link for user {user_id}: {trade_link}")

# Run the bot
bot.run(DISCORD_BOT_TOKEN)

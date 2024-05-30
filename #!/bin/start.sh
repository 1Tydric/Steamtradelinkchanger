#!/bin/bash

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Run the bot
python bot.py

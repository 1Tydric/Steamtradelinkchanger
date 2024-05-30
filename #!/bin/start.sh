#!/bin/bash

# Load environment variables
export $(grep -v '^#' .env | xargs)

chmod +x start.sh

# Run the bot
python bot.py

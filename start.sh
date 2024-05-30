# start.sh
#!/bin/bash

# Set execute permissions on this script (no-op if already executable)
chmod +x "$0"

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Run the bot
python bot.py

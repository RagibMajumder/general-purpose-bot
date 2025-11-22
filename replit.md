# Discord Bot Project

## Overview
This is a Discord bot built with discord.py that provides various utility commands including:
- QR code generation
- Math operations (addition, division, multiplication, remainder)
- Currency conversion using real-time exchange rates
- GDP data lookup via World Bank API
- Pokémon information lookup via PokéAPI
- Random communist/anticommunist leader names
- Custom user mentions and responses

## Recent Changes
- **2024-11-22**: Initial project setup in Replit environment
  - Installed Python 3.11 and all required dependencies
  - Configured Discord Bot workflow to run main.py
  - Bot token stored securely in Replit Secrets as TOKEN
  - Bot successfully connected to Discord gateway
  - Configured VM deployment for 24/7 always-on operation

## Project Architecture
- **Language**: Python 3.11
- **Main Framework**: discord.py (v2.6.4)
- **Entry Point**: `main.py`
- **Bot Prefix**: `!` (e.g., `!helpme`)

### Key Dependencies
- `discord.py` - Discord bot framework
- `qrcode` - QR code generation
- `requests` - HTTP requests for APIs
- `wbgapi` - World Bank API data access
- `aiohttp` - Async HTTP client
- `pillow` - Image processing

### Bot Commands
Use `!helpme` in Discord to see all available commands.

## Configuration
- **Bot Token**: Stored in Replit Secrets as `TOKEN`
- **Workflow**: "Discord Bot" runs `python main.py`
- **Output Type**: Console (no web interface)

## Running the Bot
The bot runs automatically via the configured workflow. It will:
1. Connect to Discord using the TOKEN secret
2. Listen for commands with the `!` prefix
3. Respond to various utility commands

### Development Mode
In development, the bot stays active for 15 minutes of inactivity before going idle. It will restart when you open the Repl.

### Production Deployment
For 24/7 operation, deploy the bot using the Deploy button:
- **Deployment Type**: VM (Reserved Virtual Machine)
- **Run Command**: `python main.py`
- **Uptime**: Continuous 99.9% availability
- The bot will maintain a constant connection to Discord and respond to commands anytime

## Files
- `main.py` - Main bot code with all commands and event handlers
- `Procfile` - Original Heroku deployment config (not used in Replit)
- `requirements.txt` - Python dependencies list (has encoding issues but dependencies installed)

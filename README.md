# Discord Autodelete Bot

This is a simple Discord bot designed to automatically delete messages older than 7 days from all text channels in the Discord servers it is a part of. This helps in maintaining server hygiene and managing message clutter.

## Features

-   **Automatic Message Deletion**: Deletes messages older than 7 days.
-   **Channel Iteration**: Shuffles channels to ensure fair processing.
-   **Docker Support**: Easy deployment using Docker and Docker Compose.

## Prerequisites

-   Python 3.9+
-   `discord.py` library
-   A Discord Bot Token

## Setup

### 1. Create a Discord Bot and Get a Token

Follow the official Discord guide to create a bot application and obtain your bot token:
[Discord Bot Documentation](https://discord.com/developers/docs/intro)

### 2. Installation

Clone this repository:

```bash
git clone https://github.com/your-username/discord-autodelete.git
cd discord-autodelete
```

### 3. Configuration

Set your Discord bot token as an environment variable.

**Linux/macOS:**
```bash
export DISCORD_TOKEN="YOUR_BOT_TOKEN_HERE"
```

**Windows (Command Prompt):**
```bash
set DISCORD_TOKEN="YOUR_BOT_TOKEN_HERE"
```

**Windows (PowerShell):**
```powershell
$env:DISCORD_TOKEN="YOUR_BOT_TOKEN_HERE"
```

Replace `YOUR_BOT_TOKEN_HERE` with your actual bot token.

## Running the Bot

### Using Docker Compose (Recommended)

Ensure you have Docker and Docker Compose installed.

1.  Create a `.env` file in the project root with your Discord token:
    ```
    DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
    ```
2.  Run the bot using Docker Compose:
    ```bash
    docker-compose up --build -d
    ```
    This will build the Docker image and start the bot in detached mode.

### Manually

1.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the bot:
    ```bash
    python bot.py
    ```

## Contributing

Feel free to fork the repository, make improvements, and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
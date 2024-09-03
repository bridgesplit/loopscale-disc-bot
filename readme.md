# Discord Bot Setup Guide

This guide will help you set up and run the Discord bot with integration to LoopScale.

## Prerequisites

- Python 3.x installed on your machine.
- A Discord Developer Bot Token.
- A LoopScale API Key.

## Setting up the Bot

1. **Add a `.env` File:**
   - Create a `.env` file in the root folder of your project.
   - Add the following environment variables to the file:

     ```env
     BOT_TOKEN=
     LOOPSCALE_API_KEY=
     ```

2. **Insert Tokens:**
   - **Discord Bot Token:** 
     - Obtain your bot token by creating a new Discord application [here](https://discord.com/developers/applications).
     - Ensure the bot has the necessary permissions: `Manage Roles`, `View Channels`, `Send Messages`, and `Use Slash Commands`. You can also grant `Administrator` permission, though it is not mandatory.
     - Add the bot token to the `BOT_TOKEN` variable in your `.env` file.
   - **LoopScale API Key:**
     - Insert your LoopScale API key into the `LOOPSCALE_API_KEY` variable in the `.env` file.

3. **Create a Virtual Environment (Recommended):**
    - Although not mandatory, it's recommended to create a virtual environment for your project to manage dependencies and avoid conflicts with other Python projects.
    - You can create a virtual environment using the following command:
        ```bash
        python -m venv venv
        ```
    - Activate the virtual environment:
        - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

        - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. **Install Required Packages:**
  - Once the virtual environment is activated, install the required Python packages using the following command:

    ```bash
    pip install -r requirements.txt
    ```
    
5. **Configure Role ID:**
   - Open the `settings.py` file.
   - Set the `CLAIM_ROLE_ID` variable with the role ID you wish to assign to users who reach 10,000 points.
   - **Important:** Ensure that this role is lower in the role hierarchy than the bot's role in Discord, or the bot will not be able to assign it.

6. **Run the Bot:**
   - Start the bot using the following command:

     ```bash
     python main.py
     ```

7. **Sync Commands:**
   - To make the bot's commands available for use, send the following message to the bot in a direct message (DM):
   
     ```bash
     -vmpsync
     ```

   - This is a one-time setup step that needs to be done before users can start using the bot's commands.

## Available Commands

- **`/leaderboard`**: Displays the leaderboard for the top 10 members by points or waitlist rank.
- **`/points`**: Shows the points of a specific user.
- **`/waitlist-rank`**: Displays the waitlist rank of a specific user.

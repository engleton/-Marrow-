# --- Main Bot Script: hecate_bot.py ---

import platform
import random
import datetime
import os
import logging
import subprocess
import sys
import asyncio
import aiohttp  # Keep import

# --- Required Imports ---
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import Context
# from dotenv import load_dotenv (Removed duplicate import)

# --- Music Cog Imports ---
import requests
import yt_dlp

# --- Gemini AI Import ---
import google.generativeai as genai

# --- Setup Logging ---
log_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
log_file_handler = logging.FileHandler(filename='discord_bot.log', encoding='utf-8', mode='w')
log_file_handler.setFormatter(log_formatter)
log_console_handler = logging.StreamHandler()
log_console_handler.setFormatter(log_formatter)
# Configure root logger to add handlers
logging.basicConfig(level=logging.INFO, handlers=[log_file_handler, log_console_handler])
initial_logger = logging.getLogger('InitialSetup')
initial_logger.setLevel(logging.INFO)

initial_logger.info("--- Logging initialized ---")
# Removed unused and unresolved import "Pla"
import random
import datetime
import os
import logging
import subprocess
import sys
import asyncio
import aiohttp # Keep import

# --- Required Imports ---
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv

# --- Music Cog Imports ---
import requests
import yt_dlp

# --- Gemini AI Import ---
import google.generativeai as genai

# --- Setup Logging ---
log_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
log_file_handler = logging.FileHandler(filename='discord_bot.log', encoding='utf-8', mode='w')
log_file_handler.setFormatter(log_formatter)
log_console_handler = logging.StreamHandler()
log_console_handler.setFormatter(log_formatter)
# Configure root logger to add handlers
logging.basicConfig(level=logging.INFO, handlers=[log_file_handler, log_console_handler])
initial_logger = logging.getLogger('InitialSetup')
initial_logger.setLevel(logging.INFO)

initial_logger.info("--- Logging initialized ---")

# --- Load Environment Variables ---
initial_logger.info("Starting to load environment variables...")
# Ensure environment variables are loaded only once
# Removed duplicate load_dotenv() and redundant environment variable loading

initial_logger.info("Finished loading environment variables.")

# --- Load Environment Variables ---
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# --- Fatal Error/Warning Checks ---
if not TOKEN:
    initial_logger.error("FATAL ERROR: DISCORD_BOT_TOKEN not set.")
    sys.exit(1)
YOUR_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID", "YOUR_CLIENT_ID_HERE")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Ensure GOOGLE_API_KEY is defined here
if not YOUR_CLIENT_ID or YOUR_CLIENT_ID == "YOUR_CLIENT_ID_HERE":
    initial_logger.warning("DISCORD_CLIENT_ID not set.")
    YOUR_CLIENT_ID = "0"
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    initial_logger.warning("Spotify credentials not set. Spotify features may fail.")
try:
    raw_auth_id = os.getenv("AUTHORIZED_USER_ID")
    AUTHORIZED_USER_ID = int(raw_auth_id) if raw_auth_id else None  # None if not set
except ValueError:
    initial_logger.warning("AUTHORIZED_USER_ID in .env is not a valid integer. Owner/Music commands may not work as expected.")
    AUTHORIZED_USER_ID = None  # Treat invalid as not set

if not AUTHORIZED_USER_ID:
    initial_logger.warning("AUTHORIZED_USER_ID not set. Owner/Music commands may be restricted or unusable.")
if not GOOGLE_API_KEY:
    initial_logger.warning("GOOGLE_API_KEY not set. Gemini features disabled.")

initial_logger.info("Fatal error/warning checks complete.")

# --- Configure Google AI ---
initial_logger.info("Starting to configure Google AI...")
if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        initial_logger.info("Google AI SDK configured successfully.")
    except Exception as e:
        initial_logger.error(f"Failed to configure Google AI SDK: {e}")
        GOOGLE_API_KEY = None  # Signal Gemini is unavailable
else:
    initial_logger.warning("Google AI Key missing, skipping config.")

initial_logger.info("Finished configuring Google AI.")
initial_logger.info("Loading environment variables...")
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
YOUR_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID", "YOUR_CLIENT_ID_HERE")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
try:
    raw_auth_id = os.getenv("AUTHORIZED_USER_ID")
    AUTHORIZED_USER_ID = int(raw_auth_id) if raw_auth_id else None  # None if not set
except ValueError:
    initial_logger.warning("AUTHORIZED_USER_ID in .env is not a valid integer. Owner/Music commands may not work as expected.")
    AUTHORIZED_USER_ID = None  # Treat invalid as not set

initial_logger.info("Environment variables loaded.")

# --- Fatal Error/Warning Checks ---
if not TOKEN:
    initial_logger.error("FATAL ERROR: DISCORD_BOT_TOKEN not set.")
    sys.exit(1)
if not YOUR_CLIENT_ID or YOUR_CLIENT_ID == "YOUR_CLIENT_ID_HERE":
    initial_logger.warning("DISCORD_CLIENT_ID not set.")
    YOUR_CLIENT_ID = "0"
if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    initial_logger.warning("Spotify credentials not set. Spotify features may fail.")
if not AUTHORIZED_USER_ID:
    initial_logger.warning("AUTHORIZED_USER_ID not set. Owner/Music commands may be restricted or unusable.")
if not GOOGLE_API_KEY:
    initial_logger.warning("GOOGLE_API_KEY not set. Gemini features disabled.")

initial_logger.info("Fatal error/warning checks complete.")

# --- Configure Google AI ---
initial_logger.info("Configuring Google AI...")
if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        initial_logger.info("Google AI SDK configured successfully.")
    except Exception as e:
        initial_logger.error(f"Failed to configure Google AI SDK: {e}")
        GOOGLE_API_KEY = None  # Signal Gemini is unavailable
else:
    initial_logger.warning("Google AI Key missing, skipping config.")

initial_logger.info("--- Initial Setup Complete ---")

# --- Define Intents ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True

initial_logger.info("Intents defined.")

# --- Instantiate Bot ---
try:
    initial_logger.info("Starting bot...")
    bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)
    bot.bot_prefix = BOT_PREFIX
    bot.run(TOKEN)
except Exception as e:
    initial_logger.error(f"Bot failed to start: {e}")
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)
bot.bot_prefix = BOT_PREFIX
initial_logger.info("Bot instantiated.")
log_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
log_file_handler = logging.FileHandler(filename='discord_bot.log', encoding='utf-8', mode='w')
log_file_handler.setFormatter(log_formatter)
log_console_handler = logging.StreamHandler()
log_console_handler.setFormatter(log_formatter)
# Configure root logger to add handlers
logging.basicConfig(level=logging.INFO, handlers=[log_file_handler, log_console_handler])
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.INFO)
bot_logger = logging.getLogger('HecateBot') # General Bot Logger
bot_logger.setLevel(logging.INFO)
# Removed duplicate load_dotenv() call
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
YOUR_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID", "YOUR_CLIENT_ID_HERE")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
try:
    raw_auth_id = os.getenv("AUTHORIZED_USER_ID")
    AUTHORIZED_USER_ID = int(raw_auth_id) if raw_auth_id else None # None if not set
except ValueError:
    print("WARNING: AUTHORIZED_USER_ID in .env is not a valid integer. Owner/Music commands may not work as expected.")
    AUTHORIZED_USER_ID = None # Treat invalid as not set
    AUTHORIZED_USER_ID = None # Treat invalid as not set

# --- Fatal Error/Warning Checks ---
if not TOKEN: print("FATAL ERROR: DISCORD_BOT_TOKEN not set."); sys.exit(1)
if not YOUR_CLIENT_ID or YOUR_CLIENT_ID == "YOUR_CLIENT_ID_HERE": print("WARNING: DISCORD_CLIENT_ID not set."); YOUR_CLIENT_ID = "0"
if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET: print("WARNING: Spotify credentials not set. Spotify features may fail.")
if not AUTHORIZED_USER_ID: print("WARNING: AUTHORIZED_USER_ID not set. Owner/Music commands may be restricted or unusable.")
if not GOOGLE_API_KEY: print("WARNING: GOOGLE_API_KEY not set. Gemini features disabled.")

# --- MacGruger Configuration ---
MACGRUGER_DISCORD_BOTS_DIR = os.path.expanduser("~/Library/MacGruger/DiscordBots")
MACGRUGER_PROMPTS_BASE_PATH = "/Users/claytonwade/Documents/DiscordMain/Prompts/Awesome_GPT_Super_Prompting/" # Updated Path




# --- Configure Google AI ---
if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        bot_logger.info("Google AI SDK configured successfully.")
    except Exception as e:
         bot_logger.error(f"Failed to configure Google AI SDK: {e}")
         GOOGLE_API_KEY = None # Signal Gemini is unavailable
# --- Define Intents ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True

# --- Print to indicate end of setup ---
print("Script reached end of initial setup.")

# --- Instantiate Bot ---
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)
bot.bot_prefix = BOT_PREFIX

# --- Define Intents ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True

# --- Print to indicate end of setup ---
print("Script reached end of initial setup.")
# --- Instantiate Bot ---
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)
bot.bot_prefix = BOT_PREFIX
MUSIC_PERMISSIONS = 326424916992 # Includes Voice perms
# Ensure Client ID is integer for URL generation
try: client_id_int = int(YOUR_CLIENT_ID)
except ValueError: client_id_int = 0; bot_logger.error("Invalid DISCORD_CLIENT_ID format, using 0.")
bot.invite_link = discord.utils.oauth_url(client_id_int, permissions=discord.Permissions(permissions=MUSIC_PERMISSIONS), scopes=("bot", "applications.commands"))

# --- Cog Definition: Hecate (General, MacGruger, AI Commands) ---
class FeedbackForm(discord.ui.Modal, title="Feedback"):
    feedback = discord.ui.TextInput(label="What do you think about this bot?", style=discord.TextStyle.long, placeholder="Type here...", required=True, max_length=256)
    async def on_submit(self, i: discord.Interaction): self.interaction=i; self.answer=str(self.feedback.value); self.stop() # Use .value

class Hecate(commands.Cog, name="hecate"):
    def __init__(self, bot_instance: commands.Bot) -> None:
        self.bot = bot_instance
        self.logger = logging.getLogger('HecateCog')
        self.logger.setLevel(logging.INFO)
        global log_file_handler, log_console_handler
        if log_file_handler not in self.logger.handlers: self.logger.addHandler(log_file_handler)
        if log_console_handler not in self.logger.handlers: self.logger.addHandler(log_console_handler)
        self.logger.propagate = False

        self.analysis_file1 = "data_to_analyze.txt"
        self.analysis_file2 = "gemini jb.txt"
        # Gemini Model Init
        self.gemini_model = None
        if GOOGLE_API_KEY:
            try: self.gemini_model = genai.GenerativeModel('gemini-pro'); self.logger.info("Initialized Gemini Pro model.")
            except Exception as e: self.logger.error(f"Failed to initialize Gemini model: {e}")
        else: self.logger.warning("Gemini features disabled (missing API key).")
        # MacGruger Dir Checks
        try:
            os.makedirs(MACGRUGER_DISCORD_BOTS_DIR, exist_ok=True); self.logger.info(f"Checked MacGruger bots dir: {MACGRUGER_DISCORD_BOTS_DIR}")
            if not os.path.isdir(MACGRUGER_PROMPTS_BASE_PATH): self.logger.warning(f"MacGruger Prompts Base path not found: {MACGRUGER_PROMPTS_BASE_PATH}")
        except OSError as e: self.logger.error(f"Error creating MacGruger dir {MACGRUGER_DISCORD_BOTS_DIR}: {e}")
        # Context Menus
        self.context_menu_user = app_commands.ContextMenu(name="Grab ID", callback=self.grab_id); self.bot.tree.add_command(self.context_menu_user)
        self.context_menu_message = app_commands.ContextMenu(name="Remove spoilers", callback=self.remove_spoilers); self.bot.tree.add_command(self.context_menu_message)

    # --- Helper Functions ---
    async def _run_blocking_subprocess(self, command_args):
        if not isinstance(command_args, list): self.logger.error(f"Subprocess helper received non-list: {command_args}"); raise TypeError("command_args must be a list")
        try:
            process = await asyncio.to_thread(subprocess.run, command_args, check=True, capture_output=True, text=True, timeout=120)
            stdout_preview = (process.stdout[:1000] + '...' if len(process.stdout) > 1000 else process.stdout) or '(No output)'
            return True, f"Command executed.\nOutput:\n```\n{stdout_preview}\n```"
        except subprocess.CalledProcessError as e:
            stderr_preview = (e.stderr[:1000] + '...' if len(e.stderr) > 1000 else e.stderr) or '(No error output)'
            error_msg = f"Command failed (Code {e.returncode}).\nError:\n```\n{stderr_preview}\n```"; self.logger.error(f"Subprocess error for {' '.join(command_args)}: {error_msg}"); return False, error_msg
        except subprocess.TimeoutExpired: error_msg = "Command timed out (120s)."; self.logger.error(f"Subprocess timeout: {' '.join(command_args)}"); return False, error_msg
        except FileNotFoundError: error_msg = f"Error: Command '{command_args[0]}' not found."; self.logger.error(f"Subprocess FileNotFoundError: {command_args[0]}"); return False, error_msg
        except Exception as e: error_msg = f"Unexpected subprocess error: {e}"; self.logger.exception(f"Unexpected error running subprocess {' '.join(command_args)}"); return False, error_msg

    async def install_bot_internal(self, repo_url, bot_name):
        self.logger.info(f"Install bot '{bot_name}' from '{repo_url}'")
        bot_path = os.path.join(MACGRUGER_DISCORD_BOTS_DIR, bot_name)
        if os.path.exists(bot_path) and os.listdir(bot_path): self.logger.warning(f"Install aborted: Dir '{bot_path}' exists and not empty."); return False, f"Error: Dir `{bot_name}` exists and not empty."
        os.makedirs(os.path.dirname(bot_path), exist_ok=True); command = ["git", "clone", repo_url, bot_path]
        success, message = await self._run_blocking_subprocess(command)
        if success: self.logger.info(f"Installed bot '{bot_name}' to '{bot_path}'"); return True, f"Bot '{bot_name}' installed:\n`{bot_path}`"
        else: self.logger.error(f"Failed install bot '{bot_name}': {message}"); return False, f"Error installing '{bot_name}': {message}"

    async def download_github_file_internal(self, file_url, destination_path):
        self.logger.info(f"Download '{file_url}' to '{destination_path}'")
        safe_base_dir = os.path.abspath(MACGRUGER_DISCORD_BOTS_DIR); abs_destination = os.path.abspath(destination_path)
        if os.path.commonpath([safe_base_dir]) != os.path.commonpath([safe_base_dir, abs_destination]): self.logger.warning(f"Path traversal blocked: {destination_path}"); return False, "Error: Invalid destination path."
        os.makedirs(os.path.dirname(abs_destination), exist_ok=True); command = ["curl", "-sfL", file_url, "-o", abs_destination]
        success, message = await self._run_blocking_subprocess(command)
        if success: self.logger.info(f"Downloaded '{file_url}' to '{abs_destination}'"); return True, f"File downloaded:\n`{abs_destination}`"
        else:
            self.logger.error(f"Failed download '{file_url}': {message}")
            if os.path.exists(abs_destination):
                 try:
                     os.remove(abs_destination)
                     self.logger.info(f"Removed partially downloaded file: {abs_destination}")
                 except OSError as rm_err:
                     self.logger.warning(f"Could not remove partially downloaded file {abs_destination}: {rm_err}")
            return False, f"Error downloading: {message}"

    def ask_awesome_gpt_internal(self, query=None, use_keyword=False):
        base_prompt_path = MACGRUGER_PROMPTS_BASE_PATH; self.logger.info(f"Fetching prompt from '{base_prompt_path}'. Q:'{query}', KW:{use_keyword}")
        if not os.path.isdir(base_prompt_path): self.logger.error(f"Prompt base path not found: {base_prompt_path}"); return f"Error: Prompt directory missing (`{base_prompt_path}`)."
        all_md_files = [];
        try:
            for dirpath, dirnames, filenames in os.walk(base_prompt_path):
                dirnames[:] = [d for d in dirnames if not d.startswith('.')];
                for filename in filenames:
                    if filename.endswith(".md"): full_path = os.path.join(dirpath, filename); relative_path = os.path.relpath(full_path, base_prompt_path); all_md_files.append({"full_path": full_path, "filename": filename, "relative_path": relative_path})
        except OSError as e: self.logger.error(f"Error walking prompt dir {base_prompt_path}: {e}"); return f"Error accessing prompt dir: {e}"
        if not all_md_files: self.logger.warning(f"No '.md' files found in {base_prompt_path}"); return f"No prompt files (.md) found in `{base_prompt_path}`."
        chosen_file_info = None; target_files = all_md_files
        if use_keyword and query:
            matching_files = [f for f in all_md_files if query.lower() in f['filename'].lower()]
            if matching_files: target_files = matching_files; self.logger.info(f"Found {len(matching_files)} matching '{query}'.")
            else: self.logger.info(f"No prompts match keyword '{query}'."); return f"No prompts found matching keyword: `{query}`."
        if not target_files: self.logger.error("Logical error: target_files became empty"); return "Error selecting prompt file (no matches?)."
        chosen_file_info = random.choice(target_files); self.logger.info(f"Selected prompt: {chosen_file_info['relative_path']}")
        if chosen_file_info:
            try:
                with open(chosen_file_info['full_path'], 'r', encoding='utf-8') as f: prompt = f.read()
                self.logger.info(f"Read prompt from {chosen_file_info['full_path']}")
                prompt_snip = prompt[:1800] + "\n... (prompt truncated)" if len(prompt) > 1800 else prompt
                return f"**Prompt:** `{chosen_file_info['relative_path']}`\n```md\n{prompt_snip}\n```"
            except Exception as e: self.logger.exception(f"Error reading prompt file {chosen_file_info['full_path']}"); return f"Error reading `{chosen_file_info['relative_path']}`: {e}"
        else: self.logger.error("Logical error: chosen_file_info is None"); return "Error selecting prompt."

    # --- Context Menus ---
    async def remove_spoilers(self, interaction: discord.Interaction, message: discord.Message) -> None:
        spoiler_attachment=None; spoiler_attachment_url=None
        for a in message.attachments:
            if a.is_spoiler(): spoiler_attachment=a; spoiler_attachment_url=a.url; break
        embed = discord.Embed(title="Message without spoilers", description=message.content.replace("||",""), color=0x9B59B6)
        if spoiler_attachment and spoiler_attachment_url: embed.set_image(url=spoiler_attachment_url)
        try: await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.HTTPException as e: self.logger.error(f"Failed spoiler removal msg: {e}")

    async def grab_id(self, interaction: discord.Interaction, user: discord.User) -> None:
        embed = discord.Embed(description=f"ID of {user.mention}: `{user.id}`.", color=0x9B59B6)
        try: await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.HTTPException as e: self.logger.error(f"Failed grab ID msg: {e}")

    # --- Hybrid Commands ---
    @commands.hybrid_command(name="help", description="List commands.")
    async def help(self, context: Context) -> None:
        embed = discord.Embed(title="Hecate Bot Help", description="List of available commands:", color=0x9B59B6)
        is_owner = await self.bot.is_owner(context.author)
        for cog_name in self.bot.cogs:
            cog = self.bot.get_cog(cog_name)
            if not cog: continue
            cog_commands = cog.get_commands()
            data = []
            for command in cog_commands:
                if isinstance(command, (app_commands.ContextMenu)): continue
                try:
                    can_run = await command.can_run(context)
                    is_owner_cmd = any(isinstance(check, type(commands.is_owner())) for check in command.checks)
                    if (command.hidden or is_owner_cmd) and not is_owner: continue
                    if not can_run: continue
                except commands.CommandError: continue
                desc = command.short_doc or command.description or "No description"
                desc_line = desc.partition("\n")[0]
                cmd_mention = f"`/{command.name}`" if isinstance(command, (commands.HybridCommand, app_commands.Command)) else f"`{self.bot.bot_prefix}{command.name}`"
                data.append(f"{cmd_mention} - {desc_line}")
            if data:
                help_text = "\n".join(sorted(data))
                embed.add_field(name=cog_name.capitalize(), value=help_text, inline=False)
        try: await context.send(embed=embed)
        except discord.HTTPException as e: self.logger.error(f"Failed help msg: {e}")

    @commands.hybrid_command(name="botinfo", description="Get bot info.")
    async def botinfo(self, context: Context) -> None:
        embed = discord.Embed(description="Based on [Krypton's](https://krypton.ninja) template", color=0x9B59B6)
        try: app_info = await self.bot.application_info(); owner = app_info.owner
        except discord.HTTPException: owner = "Unavailable"
        embed.set_author(name="Bot Information")
        embed.add_field(name="Owner:", value=f"{owner}", inline=True)
        embed.add_field(name="Python Ver:", value=f"{platform.python_version()}", inline=True)
        embed.add_field(name="discord.py Ver:", value=f"{discord.__version__}", inline=True)
        embed.add_field(name="Prefix:", value=f"`/` or `{self.bot.bot_prefix}`", inline=False)
        embed.add_field(name="Ping:", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Servers:", value=f"{len(self.bot.guilds)}", inline=True)
        embed.set_footer(text=f"Requested by {context.author}")
        try: await context.send(embed=embed)
        except discord.HTTPException as e: self.logger.error(f"Failed botinfo msg: {e}")

    @commands.hybrid_command(name="serverinfo", description="Get server info.")
    async def serverinfo(self, context: Context) -> None:
        if not context.guild: await context.send("Command unavailable in DMs."); return
        guild = context.guild; roles = [r.mention for r in reversed(guild.roles) if r.name != "@everyone"]; num_roles=len(roles)
        if num_roles > 35: roles = roles[:35] + [f" (+{num_roles - 35} more)"]
        roles_str = ", ".join(roles) if roles else "None"; roles_str = roles_str[:1020] + "..." if len(roles_str) > 1020 else roles_str
        embed = discord.Embed(title=f"**Server Info: {guild.name}**", color=0x9B59B6)
        if guild.icon: embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="ID", value=guild.id, inline=True); embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
        embed.add_field(name="Created", value=discord.utils.format_dt(guild.created_at, style='F'), inline=True)
        embed.add_field(name="Members", value=f"{guild.member_count}", inline=True); embed.add_field(name="Txt Channels", value=f"{len(guild.text_channels)}", inline=True)
        embed.add_field(name="Voice Channels", value=f"{len(guild.voice_channels)}", inline=True)
        embed.add_field(name=f"Roles ({len(guild.roles)})", value=roles_str, inline=False)
        embed.set_footer(text=f"Requested by {context.author}", icon_url=context.author.display_avatar.url)
        try: await context.send(embed=embed)
        except discord.HTTPException as e: self.logger.error(f"Failed serverinfo msg: {e}")

    @commands.hybrid_command(name="ping", description="Check bot latency.")
    async def ping(self, context: Context) -> None:
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(title="🏓 Pong!", description=f"Latency: {latency}ms.", color=0x9B59B6 if latency < 300 else 0xE02B2B)
        try: await context.send(embed=embed)
        except discord.HTTPException as e: self.logger.error(f"Failed ping msg: {e}")

    @commands.hybrid_command(name="invite", description="Get bot invite link.")
    async def invite(self, context: Context) -> None:
        embed = discord.Embed(description=f"Invite me by clicking [here]({self.bot.invite_link}).", color=0x71368A)
        try: await context.author.send(embed=embed); await context.send("Invite link sent via DM!", ephemeral=True)
        except (discord.Forbidden, discord.HTTPException):
            try: await context.send(embed=embed)
            except discord.HTTPException as e: self.logger.error(f"Failed invite msg fallback: {e}")
        except Exception as e: self.logger.exception(f"Error sending invite: {e}")

    @commands.hybrid_command(name="server", description="Get support server link.")
    async def server(self, context: Context) -> None:
        support_server_link = "https://discord.gg/mTBrXyWxAF" # Example
        embed = discord.Embed(description=f"Join the support server [here]({support_server_link}).", color=0x71368A)
        try: await context.author.send(embed=embed); await context.send("Support server link sent via DM!", ephemeral=True)
        except (discord.Forbidden, discord.HTTPException):
            try: await context.send(embed=embed)
            except discord.HTTPException as e: self.logger.error(f"Failed server link fallback: {e}")
        except Exception as e: self.logger.exception(f"Error sending server link: {e}")

    # --- 8BALL AND BITCOIN COMMANDS ARE REMOVED ---

    @commands.hybrid_command(name="userinfo", description="Get user info.")
    @app_commands.describe(user="User?")
    async def userinfo(self, context: Context, user: discord.Member = None) -> None:
        target_user = user or context.author
        if isinstance(target_user, discord.User) and context.guild: member = context.guild.get_member(target_user.id); target_user = member if member else target_user
        elif not context.guild and isinstance(target_user, discord.User): await context.send("Server info unavailable in DMs."); return
        if not isinstance(target_user, discord.Member) and context.guild: await context.send("Cannot get full server info (user might not be in server)."); return
        embed = discord.Embed(title=f"User Info: {target_user.display_name}", color=target_user.color if isinstance(target_user, discord.Member) else 0x9B59B6).set_thumbnail(url=target_user.display_avatar.url)
        embed.add_field(name="Username", value=f"{target_user}", inline=True); embed.add_field(name="ID", value=target_user.id, inline=True)
        if isinstance(target_user, discord.Member): embed.add_field(name="Status", value=str(target_user.status).title(), inline=True)
        embed.add_field(name="Acc Created", value=discord.utils.format_dt(target_user.created_at, style='F'), inline=False)
        if isinstance(target_user, discord.Member):
             embed.add_field(name="Joined Server", value=discord.utils.format_dt(target_user.joined_at, style='F') if target_user.joined_at else 'Unknown', inline=False)
             roles = [r.mention for r in reversed(target_user.roles) if r.name != "@everyone"]; num_roles = len(roles)
             roles_str = (", ".join(roles[:35]) + (f" (+{num_roles-35})" if num_roles>35 else "")) if roles else "None"; roles_str = roles_str[:1020] + "..." if len(roles_str) > 1020 else roles_str
             embed.add_field(name=f"Roles ({num_roles})", value=roles_str, inline=False)
             embed.add_field(name="Highest Role", value=target_user.top_role.mention if target_user.top_role.name != "@everyone" else "None", inline=True)
             embed.add_field(name="Nickname", value=target_user.nick or "None", inline=True)
        embed.set_footer(text=f"Requested by {context.author}", icon_url=context.author.display_avatar.url)
        try: await context.send(embed=embed)
        except discord.HTTPException as e: self.logger.error(f"Failed userinfo msg: {e}")

    @commands.hybrid_command(name="avatar", description="Display avatar.")
    @app_commands.describe(user="User?")
    async def avatar(self, context: Context, user: discord.User = None) -> None:
        target_user = user or context.author
        embed = discord.Embed(title=f"{target_user.display_name}'s Avatar", color=0x9B59B6).set_image(url=target_user.display_avatar.url)
        try: await context.send(embed=embed)
        except discord.HTTPException as e: self.logger.error(f"Failed avatar msg: {e}")

    @commands.hybrid_command(name="choose", description="Choose from options.")
    @app_commands.describe(options="Options?")
    async def choose(self, context: Context, *, options: str) -> None:
        choices = []; temp_split = [opt.strip() for opt in options.split(' or ') if opt.strip()];
        for part in temp_split: choices.extend([c.strip() for c in part.split(',') if c.strip()])
        if not choices: await context.send("Provide options (comma or 'or' separated)."); return
        if len(choices) == 1: await context.send(f"Only one option: `{choices[0]}`"); return
        chosen = random.choice(choices); embed = discord.Embed(title="Decision Made", color=0x9B59B6)
        embed.add_field(name="Options", value=f"`{', '.join(choices)}`", inline=False); embed.add_field(name="Choice", value=f"**{chosen}**", inline=False)
        try: await context.send(embed=embed)
        except discord.HTTPException as e: self.logger.error(f"Failed choose msg: {e}")

    @commands.hybrid_command(name="poll", description="Create Yes/No/Shrug poll.")
    @app_commands.describe(question="Question?")
    async def poll(self, context: Context, *, question: str) -> None:
        if not question: await context.send("Provide question."); return
        embed = discord.Embed(title="📊 Poll Time!", description=f"**{question}**", color=0x9B59B6).set_footer(text=f"Poll by {context.author}")
        try:
            await context.defer()
            poll_message = await context.send(embed=embed)
            await poll_message.add_reaction("👍"); await poll_message.add_reaction("👎"); await poll_message.add_reaction("🤷")
        except discord.Forbidden: self.logger.warning(f"No reaction perm in {context.channel.id}"); await context.followup.send("I lack permission to add reactions.", ephemeral=True)
        except discord.HTTPException as e: self.logger.error(f"Failed poll creation: {e}"); await context.followup.send("Error creating poll.", ephemeral=True)

    @commands.hybrid_command(name="analyze_system_files", desc="Analyze config files.")
    @commands.is_owner()
    async def analyze_system_files(self, context: Context) -> None:
        files_to_check = [self.analysis_file1, self.analysis_file2]; errors = []; success_files = []
        for fp in files_to_check:
            try:
                if not os.path.exists(fp): errors.append(f"Not found: `{fp}`."); continue
                with open(fp, 'r', encoding='utf-8') as f: f.read(10); success_files.append(f"`{fp}`")
            except Exception as e: errors.append(f"Error `{fp}`: {e}"); self.logger.error(f"Error analyzing {fp}: {e}")
        if not errors: await context.send(f"System files OK ({', '.join(success_files)}). hello world")
        else: msg = "Analysis Errors:\n- " + "\n- ".join(errors); msg += f"\nOK: {', '.join(success_files)}" if success_files else ""; await context.send(msg[:1990])

    @commands.hybrid_command(name="install_bot", desc="Install bot via Git.")
    @app_commands.describe(repo_url="HTTPS URL", bot_name="Dir name")
    @commands.is_owner()
    async def install_bot_cmd(self, context: Context, repo_url: str, bot_name: str):
        if not repo_url.startswith("https://") or not repo_url.endswith(".git"): await context.send("Use HTTPS Git URL ending `.git`.", ephemeral=True); return
        if not bot_name or any(c in bot_name for c in r'/\.'): await context.send("Invalid bot name.", ephemeral=True); return
        await context.defer(ephemeral=True); success, message = await self.install_bot_internal(repo_url, bot_name); await context.followup.send(message, ephemeral=True)

    @commands.hybrid_command(name="download_file", desc="Download file.")
    @app_commands.describe(file_url="URL", dest_subpath="Rel path")
    @commands.is_owner()
    async def download_file_cmd(self, context: Context, file_url: str, dest_subpath: str):
        if not file_url.startswith(("http://", "https://")): await context.send("Use HTTP/HTTPS URL.", ephemeral=True); return
        if not dest_subpath or ".." in dest_subpath: await context.send("Invalid relative path.", ephemeral=True); return
        full_dest_path = os.path.join(MACGRUGER_DISCORD_BOTS_DIR, dest_subpath); await context.defer(ephemeral=True)
        success, message = await self.download_github_file_internal(file_url, full_dest_path); await context.followup.send(message, ephemeral=True)

    @commands.hybrid_command(name="ask_gpt", desc="Get random prompt.")
    @app_commands.describe(opt_query="Keywords?")
    async def ask_gpt_cmd(self, context: Context, *, opt_query: str = None):
        await context.defer(); response = self.ask_awesome_gpt_internal(query=opt_query, use_keyword=bool(opt_query));
        try: await context.followup.send(response)
        except discord.HTTPException as e:
             if e.code == 50035: await context.followup.send("Error: Prompt too long.")
             else: self.logger.warning(f"Failed ask_gpt send: {e}"); await context.followup.send("Error sending response.")

    @commands.hybrid_command(name="super_prompt", desc="Get prompt by keyword.")
    @app_commands.describe(keyword="Filename keyword")
    async def super_prompt_cmd(self, context: Context, keyword: str):
        if not keyword: await context.send("Provide keyword.", ephemeral=True); return
        await context.defer(); response = self.ask_awesome_gpt_internal(query=keyword, use_keyword=True)
        try:
            # Define the embed object before sending
            embed = discord.Embed(title="Super Prompt", description=response, color=0x9B59B6)
            await context.send(embed=embed)
        except discord.HTTPException as e:
            #
            self.logger.error(f"Failed userinfo msg: {e}")

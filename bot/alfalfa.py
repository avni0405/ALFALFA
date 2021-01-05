"""Class for managing the task."""
from discord.ext import commands  # type: ignore
import discord  # type: ignore
from decouple import config  # type: ignore
from ..db_config import configure, GLOBAL_PATH  # type: ignore
from .stats.stats import Statistics  # type: ignore
from .crud.crud import CrudOperations  # type: ignore
from .constant import USER, GUILD, CHANNEL_ID  # type: ignore
from .nsfw.nsfw import AnalyzeMessage  # type: ignore
import os
import asyncio

API_KEY = config("BOT_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)
db = configure()
embed = discord.Embed()
stats = Statistics()
crud = CrudOperations()
analyze = AnalyzeMessage()


class Alfalfa:
    """Class for Bot's functionality."""

    def __init__(self):
        """Initialize the class."""
        bot.run(API_KEY)

    @staticmethod
    @bot.event
    async def on_ready():
        """Notify when bot is ready."""
        print('We have logged in as {0.user}'.format(bot))

    @staticmethod
    @bot.event
    async def on_message(message):
        """Check message.

        Args:
            message (object): message object
        """
        response = analyze.analyze_text(message.content)
        if response >= 0.85:
            await asyncio.sleep(5)
            await message.delete()
            await message.channel.send("This message was deleted")
        await bot.process_commands(message)

    @staticmethod
    @bot.command(aliases=['create'])
    async def create_task(ctx, task):
        """Crete a task.

        Args:
            ctx (object): context object
            task (str): task name
        """
        # Add task to database
        crud.add_task(ctx.message.author.id, task)
        await ctx.send("Cheers!! task created")
        await ctx.send(file=discord.File(
            os.path.join(GLOBAL_PATH, "images", "create.jpg")))

    @staticmethod
    @bot.command(aliases=['finish'])
    async def finish_task(ctx, numbers):
        """Finish a task."""
        user_id = USER + str(ctx.message.author.id)
        point = crud.finish_task(numbers, user_id)

        await ctx.send("You made {} Point!!".format(point))
        await ctx.send("https://media.tenor.com/images/06323b78e3ace87c29ee0e3028820366/tenor.gif")

    @staticmethod
    @bot.command(aliases=['showCompleted'])
    async def show_completed_task(ctx):
        """Display completed task."""
        embed.color = discord.Colour.green()
        embed.title = "Completed Task"
        user_id = USER + str(ctx.message.author.id)
        msg_send = crud.show_completed_task(user_id)
        embed.description = msg_send
        await ctx.send(embed=embed)

    @staticmethod
    @bot.command(aliases=['showOutstanding'])
    async def view_outstanding(ctx):
        """Display outstanding tasks of the given user.

        Args:
            userid (str): unique id of user
        """
        user_id = "user_" + str(ctx.message.author.id)
        embed.color = discord.Colour.red()
        embed.title = "Outstanding Task"
        msg_send = crud.show_outstanding_task(user_id)
        embed.description = msg_send
        await ctx.send(embed=embed)

    @staticmethod
    @bot.command(aliases=["taskStats"])
    async def show_task_stats(ctx):
        """Display task stats.

        Args:
            ctx (object): context object
        """
        user_list = {}
        for guild in bot.guilds:
            for member in guild.members:
                if not member in user_list and member.name != "Alfalfa-Bot":
                    user_list.__setitem__(member.name, member.id)
        path = stats.generate_task_stats(user_list, GLOBAL_PATH)
        await ctx.send(file=discord.File(path))

    @staticmethod
    @bot.command(aliases=["stats"])
    async def show_stats(ctx):
        """Display the user stats.

        Args:
            ctx (object): context object
        """
        user_msg_info = {}
        for guild in bot.guilds:
            for member in guild.members:
                if member.name != GUILD:
                    print(member.name)
                    user_messages = []
                    channel = bot.get_channel(CHANNEL_ID)
                    user = discord.utils.find(
                        lambda m: m.id == member.id, channel.guild.members)

                    async for message in channel.history():
                        if message.author == user:
                            user_messages.append(message.content)

                    user_msg_info.__setitem__(member.name, len(user_messages))
        path = stats.generate_user_stats(user_msg_info)
        await ctx.send(file=discord.File(path))


bot.run(API_KEY)

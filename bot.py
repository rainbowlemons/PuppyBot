import os
import time
import random
import praw
import discord
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
REDDIT_CLIENT_ID = os.getenv('CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('CLIENT_SECRET')

help_command = commands.DefaultHelpCommand(no_category = 'Commands')
activity = discord.Game(name = 'In the server with friends | !help')

bot = commands.Bot(description = """
Hi! My name is Puppybot!
All my commands start with !
I joined the server to spread positivity!
""", command_prefix = '!', help_command = help_command, activity = activity)

reddit = praw.Reddit(client_id = REDDIT_CLIENT_ID,
client_secret =  REDDIT_CLIENT_SECRET,
user_agent = 'Discord Puppybot v1.0 by /u/hosunah')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@tasks.loop(hours=2)
async def make_noise():
    puppy_noises = [
        'ruff!',
        'bark!',
        'grr!',
        'woof!',
        'arf!',
        '*wags tail*',
        'awooooo',
        '*whines*',
        '*jumps excitedly*'
    ]

    message_channel1 = bot.get_channel(505502750813978626)
    #message_channel2 = bot.get_channel(695774162437799989)
    await message_channel1.send(random.choice(puppy_noises))
    #await message_channel2.send(random.choice(puppy_noises))

@make_noise.before_loop
async def before():
    await bot.wait_until_ready()

@bot.command(name = 'dog', help = 'Posts a picture of a dog from r/dogpictures!')
async def post_dog(ctx):
    post_name = "Dog for you!"
    dog_submissions = reddit.subreddit('dogpictures').hot()
    clean_submissions = []

    for submission in dog_submissions:
        if not submission.stickied and not submission.url.startswith("https://www.reddit.com/gallery/"):
            clean_submissions.append(submission)

    submission = random.choice(clean_submissions)

    em = discord.Embed(title = post_name, color = 0x3471eb)
    em.set_footer(text = f"requested by {ctx.message.author} | From r/dogpictures")
    em.set_image(url = submission.url )

    await ctx.send(embed = em)
    print(f'image from {submission.url} posted')

@bot.command(name = 'wholesome', help = 'Posts a meme from r/wholesomememes!')
async def post_wholesome(ctx):
    post_name = "Heres a wholesome meme!"
    wholesome_submissions = reddit.subreddit('wholesomememes').hot()
    clean_submissions = []

    for submission in wholesome_submissions:
        if not submission.stickied and not submission.url.startswith("https://www.reddit.com/gallery/"):
            clean_submissions.append(submission)

    submission = random.choice(clean_submissions)

    em = discord.Embed(title = post_name, color = 0x3471eb)
    em.set_footer(text = f"requested by {ctx.message.author} | From r/wholesomememes")
    em.set_image(url = submission.url )

    await ctx.send(embed = em)
    print(f'image from {submission.url} posted')

@bot.command(name = 'fetch', help = 'Plays fetch!')
async def fetching(ctx):
    outcomes = ['puppy lost the ball!', 'puppy got the ball!', 'puppy got distracted!', '*puppy brings it back*']
    response1 = '*puppy runs to get the ball*'
    response2 = random.choice(outcomes)

    await ctx.send(response1)
    time.sleep(3)
    await ctx.send(response2)

@bot.command(name = 'pet', help='Gives puppy a pet!')
async def petting(ctx):
    happy = [
    'Puppy loves you! <3',
    '*wags tail very happily*',
    'Thank you for the pets friend!',
    '*puppy kisses you*'
    ]
    response = random.choice(happy)
    await ctx.send(response)

@bot.command(name = 'speak', help = 'Makes a noise!')
async def puppy_speak(ctx):
    puppy_noises = [
        'ruff!',
        'bark!',
        'grr!',
        'woof!',
        'arf!'
    ]
    response = random.choice(puppy_noises)
    await ctx.send(response)

if __name__ == '__main__':
    make_noise.start()
    bot.run(TOKEN)

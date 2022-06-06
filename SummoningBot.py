#Andrew Tang
#Tango#5190
#Summoning Bot

import discord
import time
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

#All commands will start with '!'
client = commands.Bot(command_prefix = '!', intents = intents)

#channelID dedicated to summoning the user
#Continuous joining and leaving can be very disruptive for the other members in the voice channel
#so it's good to have a separate voice channel for joining and leaving
summoningChannel = 983460263011430430

#Indicates that the bot is ready
@client.event
async def on_ready():
    print("-------------------------------")
    print("SummoningBot is ready for use!")
    print("-------------------------------")

#Bot will respond to "!hello"
@client.command()
async def hello(ctx):
    await ctx.send("I hate you!")

#Optional member welcoming function
# @client.event
# async def on_member_join(member):
#     channel = client.get_channel(983142944192208898)
#     await channel.send("Welcome to the server!")


#Optional member leaving function
# @client.event
# async def on_member_remove(member):
#     channel = client.get_channel(983142944192208898)
#     await channel.send("Goodbye!")

#This is for if the user tries to summon while on cooldown
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Summoning is still on cooldown! Please try again in {:.2f}s".format(error.retry_after)
        await ctx.send(msg)


#This is the summoning command, "!summon @target"
@client.command(pass_context = True)
@commands.cooldown(1, 180, commands.BucketType.user)
async def summon(ctx, member: discord.Member):
    #First checks if summoner and target are in voice channels
    if (member.voice and ctx.author.voice):
        #prevChannel is the channel that the target is currently in
        prevChannel = member.voice.channel

        #channel is the dedicated summoning channel for the server. This is where the target will be moved to
        channel = client.get_channel(summoningChannel)

        #move target to summoning channel. Sleep in between move/connect/disconnect to ensure the sounds dont overlap
        await member.move_to(channel)
        time.sleep(.2)
        await channel.connect()
        #for some reason the first disconnect takes longer than the others so there is no need for a sleep command
        await ctx.guild.voice_client.disconnect()
        time.sleep(.2)
        await channel.connect()
        time.sleep(.2)
        await ctx.guild.voice_client.disconnect()
        time.sleep(.2)

        #move the target back to their original channel
        await member.move_to(prevChannel)
    #If target is not in a voice channel, we cannot summon
    elif not member.voice:
        memberName = ""
        for letter in str(member):
            if letter != '#':
                memberName += letter
            else:
                break
        await ctx.send(memberName + " is not in a voice channel!")
    #If summoner is not in a voice channel, we cannot summon (this is to help avoid summoning abuse)
    else:
        await ctx.send("You must be in a voice channel to summon!")


#Leave command in case something goes wrong with the bot
@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel")
    else:
        await ctx.send("I am not in a voice channel")

client.run('OTgzMTM5MzY1NzMzNjcxMDEy.GQfBlS.a-y4p5Sd5Dwq-qhrXvfw_7Eq4pbzmCovfIB4Ac')

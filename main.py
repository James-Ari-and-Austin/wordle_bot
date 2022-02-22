#Import Libraries
import discord
import wordle

#Variable Definition
token = "OTQyMjE3ODg2NDAxOTU3ODk4.YghSyQ.OQBVr3_pbyA-13bNdxVu8auVBzs"
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0}'.format(client.user))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.clean_content == "wordle":
        await message.channel.send("wordle time")
    #await message.channel.send("Message Recieved")

client.run(token)

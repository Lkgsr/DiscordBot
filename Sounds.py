import discord
import random
from discord.ext import commands
import os


class PlaySounds:
    def __init__(self, client):
        self.client = client

    description_play = 'All playable sounds:'
    for i in os.listdir('sounds'):
        i = i.replace('.mp3', '')
        description_play = description_play + '\n' + i

    @commands.command(description=description_play, pass_context=True)
    async def playtriggered(self, context):
        global player, voice
        counter = 0
        print(context.message.content)
        args = context.message.content.split(' ')
        if len(args) > 1:
            file = args[1] + '.mp3'
            if file in os.listdir('sounds'):
                voice = await self.client.join_voice_channel(context.message.author.voice.voice_channel)
                player = voice.create_ffmpeg_player('sounds/' + file)
                player.start()
            else:
                await self.client.say('404 sound file not found')
                return
        else:
            file = os.listdir('sounds')[random.randint(0, len(os.listdir('sounds')))]
            voice = await self.client.join_voice_channel(context.message.author.voice.voice_channel)
            player = voice.create_ffmpeg_player('sounds/' + file)
            player.start()
        while player.is_playing():
            counter += 1
        else:
            print(counter)
            await voice.disconnect()

    @commands.command(description='Stops the current playing session', pass_context=True)
    async def stop(self, context):
        global player, voice
        if player.is_playing():
            player.stop()
            voice.disconnect()
        else:
            await self.client.send_message(context.message.channel, f"Hier gibt es KEINE Musik bei der DEUTSCHENBAHN")


def setup(client):
    client.add_cog(PlaySounds(client))


'''@client.command(description='Plays a Youtube Link as Sound', pass_context=True)
async def playyoutube(context):
    global player, voice
    print(context.message.content)
    args = context.message.content.split(' ')
    counter = 0
    if len(args) > 1:
        voice = await client.join_voice_channel(context.message.author.voice.voice_channel)
        player = await voice.create_ytdl_player(args[1])
        await client.send_message(context.message.channel, f"Time for some nice Music from {player.uploader} \n"
                                                     f"with the tittle {player.title}")
        player.start()
        await player.disconnect()


@client.command(description='Joins the channel', pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)


@client.command(description='Joins the channel', pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)'''

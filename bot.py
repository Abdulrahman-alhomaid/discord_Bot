
import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get , find
import random
import os
import googleapiclient.discovery

from threading import *
import concurrent.futures
import time
import shutil
import Queue


songNum = 0
queue = {}

remangingSongs = 0
playing = False
allSongs = []
palyingSong = 0
messages = {}



def runBot(token):
    bot = commands.Bot(command_prefix='!')

    @bot.event
    async def on_ready():
        global songNum

        print("STARTING....")
        print("READY....")

    @bot.command(pass_context=True, aliases=['j'])
    async def join(ctx):
        
        channel = ctx.author.voice.channel
        voice = get(bot.voice_clients , guild=ctx.guild)
        print(voice)
        print(channel)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        

# await channel.send(file=discord.File('my_image.png'))



    @bot.event
    async def on_message(message):

        await bot.process_commands(message)
        if message.author == bot.user:
            return



    @bot.event
    async def on_raw_reaction_add(payload):
        #TODO serch msg and find the time if more than 10 sec DO NOT MARRY

        if payload.user_id == 694582007128391730:
            return

        channel = bot.get_channel(payload.channel_id)
        guild = bot.get_guild(payload.guild_id)
        author = guild.get_member(payload.user_id)
        msg = messages.get(payload.message_id)
        print("\n")
        print(channel) 
        print(guild)
        print(author)
        print(msg)
        print("\n")
        if not msg:
            return
        ctx = await bot.get_context()
        await ctx.send("YES")
        
            
        

    @bot.command(pass_context=True,aliases=['download' , 'dow'])
    async def downloadSong(ctx):
        url = 'https://2cf1b309.ngrok.io/song.mp3' 

        await ctx.send(url)

    @bot.command(pass_context=True,aliases=['w'])
    async def wa(ctx):
        # try:
        channel = ctx.channel


        random_number = random.randint(0, 8)
        detals = characters.get(random_number)

        da = " cahr name \n point $"

        embed=discord.Embed(title=str(detals.name), description=detals.des, color=0xd11515)

        embed.add_field(name=str(detals.point), value="\u200b", inline=False)  
        embed.set_image(url=detals.url)
        embed.set_footer(text="enjoy")
        message = await ctx.send(embed=embed)
        emoji = '\N{THUMBS UP SIGN}'
        # or '\U0001f44d' or '👍'
        messages.update({message.id :detals})
        await message.add_reaction(emoji)
         
        # except Exception as e:
        #     print(e)








    @bot.command(pass_context=True, aliases=['pl', 'p'])
    async def play(ctx, url: str):

        global songNum
        global playing      
        global queue 

        itIsList = False

        if playing:
            print('\n\nPLAYING\n')
            addToQueue(url , False)
            return

        else:
            if 'list' in url:
                urlElm = url.split('&')
                #print(urlElm)
                songURL = ''
                for x in urlElm:
                    if 'list' in x:
                        playListId = x[5:]
                        #print(playListId)
                    else:
                        songURL += x 

                print('creating the obj')
            
                urlsObj = GetURL(playListId )
                print('running the thread')
                
                urlsObj.start()
                itIsList = True
                print('Done i guess')
            else:
                songURL = url
            song_there = os.path.isfile("song.mp3")

            try:
                if song_there:
                    os.remove("song.mp3")
                    print("\nRemoved current song file\n")
            except PermissionError:
                print("Trying to delete song file, but it's being played\n")
                await ctx.send("ERROR: Music playing, use stop command to play new song")
                return

            voice = get(bot.voice_clients, guild=ctx.guild)
            

            # qp = queue_path  +'\\'+ "%(title)s.%(ext)s"      #   str(songNum) +'.%(ext)s' #
            # print(qp)
            ydl_opts = {
                'format': 'bestaudio/best',
                #'quiet' : True,
                #'simulate' : True,
                'ignore-errors' : True,
                # 'outtmpl' : qp,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            try:

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    print(f"Downloading audio now for => {songURL}\n")
                    ydl.download([songURL])
                    print('done downloding')
            except:
                print("FALLBACK: youtube-dl not supported, searching spotify now (This is normal if spotify URL)\n")


            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    
                    queue.update({1 : file})
                    newName = "song.mp3"
                    os.rename(file, newName)
                    songNum += 1
                    
                    voice.play(discord.FFmpegPCMAudio(newName), after=lambda e:  playQueue(2))
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 1
                    sn = queue[1]
                    await ctx.send(f"Playing: {sn}")
                    print("Playing\n")
                    playing = True

            if itIsList:

                addToQueue(url , True)
               


        def playQueue(nSongNumber):
            global playing      
            global palyingSong

            Queue_infile = os.path.isdir("./Queue")
            if Queue_infile is True:
                DIR = os.path.abspath(os.path.realpath("Queue"))
                length = len(os.listdir(DIR))
                still_q = length - 1
                try:
                    snName = str(nSongNumber) + '.mp3'
                    first_file = os.listdir(DIR)[0]
                except:
                    print("No more queued song(s)\n")
                    playing = False
                   
                    return
                main_location = os.path.dirname(os.path.realpath(__file__))
                song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
                if length != 0:
                    print("Playing next queued\n")
                    print(f"Songs still in queue: {still_q}\n")
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")
                    shutil.move(song_path, main_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            name = file
                            os.rename(file, 'song.mp3')
                    ns = nSongNumber + 1  
                    palyingSong += 1       
                    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e:  playQueue(ns))
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.07
                    songName = queue[nSongNumber]
                    print(f"Playing: {songName}")
                    #await ctx.send(f"Playing: {songName}")
                else:
                    
                    return
            else:
                
                print("End\n")
    
    def down(songURL , snDown):
        

        global queue 
        print('\n\nIN THREAD DOWNLOADING ')
        queue_path = os.path.abspath(os.path.realpath("./Temp"))
        qp = queue_path  +'\\'+  str(snDown) +'\\'+'%(title)s.%(ext)s' 
        print(qp)
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet' : True,
            #'simulate' : True,
            'ignore-errors' : True,
            'outtmpl' : qp,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading audio now for => {songURL}\n")
                ydl.download([songURL])
                print('done downloding')
        except:

            print("FALLBACK: youtube-dl not supported, searching spotify now (This is normal if spotify URL)\n")
        
        for f in os.listdir("./Temp"):
            # print(f'file is {f} and the song number is {snDown} ')
            # print(f'file type is {type(f)} and the song number type is {type(snDown)} ')
            if f == str(snDown):
         
                main_location = os.path.dirname(os.path.realpath(__file__))
                fPath = main_location +'\\Temp\\'+str(snDown)
                print(f'the path we are loing in is {fPath}')
                for file in os.listdir(fPath):
                    
                    if file.endswith(".mp3"):

                        queue.update({snDown : file})
                        
                        fp = fPath +"\\"+ file
                        
                        
                        newName = main_location +"\\Queue\\"+ f + ".mp3"
                        print('\n')
                        print(f'the ps is {fp} ')
                        print(f'the newName is {newName}')
                        print('\n')
                        if os.path.isfile(newName):
                            print(f'deleteing {newName}')
                            os.remove(newName)
                        os.rename(fp, newName)
                        os.rmdir(fPath)


    def addToQueue(songLink, isFierst):

        
        global songNum
 
        
        
 
        songURL = songLink
        if 'list' in songLink:
            print('it is list')
            urlElm = songLink.split('&')
            songURL = ''
            for x in urlElm:
                if 'list' in x:
                    playListId = x[5:]
                else:
                    songURL += x 
                     
            print(f'the play list id is {playListId}' )
            print(f'the new URL is  {songURL}' )
            
            urlsObj = GetURL(playListId)
            urlsObj.start()
            urls = urlsObj.join()
            print(urls)

            nLink = 'https://www.youtube.com/watch?v='
            
            downDec = {}
            for link in urls:
                if not isFierst:
                    l = nLink + link
                    songNum += 1
                    downDec.update({songNum : l})
                else:
                    isFierst = False 
                  

            with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:

                ur = {executor.submit(down, downDec[key], key): key for key in downDec}
                for future in concurrent.futures.as_completed(ur):
                    pass

    

        else:
            queue_path = os.path.abspath(os.path.realpath("./Temp"))
            songNum += 1 
            qp = queue_path  +'\\'+ '%(title)s.%(ext)s' 
            print(qp)
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet' : True,
                #'simulate' : True,
                'ignore-errors' : True,
                'outtmpl' : qp,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    print(f"Downloading audio now for => {songURL}\n")
                    ydl.download([songURL])
                    print('done downloding')
            except:

                print("FALLBACK: youtube-dl not supported, searching spotify now (This is normal if spotify URL)\n")
            print(songNum)
            for file in os.listdir("./Temp"):
                if file.endswith(".mp3"):
                    main_location = os.path.dirname(os.path.realpath(__file__))
                    fp = main_location +'\\Temp\\' + file
                    print(fp)
                    queue.update({songNum : file})
                    newName = main_location +"\\Queue\\"+ str(songNum) + ".mp3"
                    
                    if os.path.isfile(newName):
                        print(f'deleteing {newName}')
                        os.remove(newName)
                    os.rename(fp, newName)
       
        

    @bot.command(pass_context=True,aliases=['pa'])
    async def pause(ctx):

        voice = get(bot.voice_clients , guild=ctx.guild)
        if voice and voice.is_playing():
            print('Music pused')
            voice.pause()
            await ctx.send('Music is paused')
        else:
            print('nothing to pause')
            await ctx.send('nothing to pause')

    @bot.command(pass_context=True,aliases=['r', 'res'])
    async def resume(ctx):

        voice = get(bot.voice_clients , guild=ctx.guild)
        if voice and voice.is_paused():
            print('resumming')
            voice.resume()  
            await ctx.send('resumming')
        else:
            print('nothing tp resume')
            await ctx.send('nothing to resume')



    @bot.command(pass_context=True,aliases=['st'])
    async def stop(ctx):
        global playing 
        
        
        voice = get(bot.voice_clients , guild=ctx.guild)
        if voice and voice.is_playing():
            print('Music stop')
            playing = False
            voice.stop()
            await ctx.send('Music is stop')
        else:
            print('nothing to stop')
            await ctx.send('nothing to stop')

 
    bot.run(token)



class GetURL(Thread):
    
    def __init__(self, playListID=""):
        super(GetURL, self).__init__()
        print('constroctor')
        self.playListID = playListID
        self.urls = None
        
	    
    
    def run(self):
        print('runn')
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "add youtube dev key or add to .env file"
        pageToken = ''
        first = True
        self.urls= []
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = DEVELOPER_KEY)
    
        request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=5,
        playlistId=self.playListID
        )
        
        response = request.execute()

        try:
            pageToken  = response['nextPageToken']
        except:
            pageToken = False
        
        for itme in response['items']:
            self.urls.append(itme['snippet']['resourceId']['videoId'])
        print(pageToken)

        while pageToken :
            print(pageToken)
            request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                maxResults=50,
                pageToken=pageToken,
                playlistId=self.playListID
            )
            response = request.execute()
            try:
                pageToken  = response['nextPageToken']
            except:
                pageToken = False

            for itme in response['items']:
                self.urls.append(itme['snippet']['resourceId']['videoId'])

        print(self.urls)
        

    def join(self):
        Thread.join(self)
        return self.urls

class DownloadURL(Thread):
    
    def __init__(self, url="" , songNum=None):

        super(DownloadURL, self).__init__()
        print('constroctor')
        self.songNum = songNum
        self.url = url
        

    def run(self):



        global queue 

        queue_path = os.path.abspath(os.path.realpath("./Temp"))
        qp = queue_path  +'\\'+  str(self.songNum) +'\\'+'%(title)s.%(ext)s' 
        print(qp)
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet' : True,
            #'simulate' : True,
            'ignore-errors' : True,
            'outtmpl' : qp,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading audio now for => {songURL}\n")
                ydl.download([songURL])
                print('done downloding')
        except:

            print("FALLBACK: youtube-dl not supported, searching spotify now (This is normal if spotify URL)\n")
        
        for f in os.listdir("./Temp"):
            if f == songNum:
                for file in f:
                    if file.endswith(".mp3"):
                        main_location = os.path.dirname(os.path.realpath(__file__))
                        fp = main_location +'\\Temp\\'+str(songNum) + file
                        print(fp)
                        queue.update({songNum : file})
                        newName = main_location +"\\Queue\\"+ str(songNum) + ".mp3"
                        
                        if os.path.isfile(newName):
                            print(f'deleteing {newName}')
                            os.remove(newName)
                        os.rename(fp, newName)
 
        

if __name__ == "__main__":
    
    token = "add token here or in .env file"
    
    runBot(token)

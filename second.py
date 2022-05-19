from time import sleep
from mcstatus import JavaServer
import discord

import boto3


client = discord.Client()
TOKEN = 'OTc2NzQwODc4MTc1NTk2NTQ0.G43F9J.rpZjAUco9HU4Lugok6gEw59Va-P1PYl_2EjQ8w'


ec2 = boto3.resource('ec2', "eu-central-1",
            aws_access_key_id="AKIASEOUW2XHKWF4Y2BL",
            aws_secret_access_key= "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")

instance = ec2.Instance("i-0cde512d5bcdbf8d0")


server = JavaServer.lookup("35.157.209.70")


def get_current_players():
    try: 
        return server.status().players.online
    except Exception as e:
        print(e)
        return 0

def start():
    print(instance.start())

def stop():
    print(instance.stop())



async def count_down_loop(channel):
    countdown = 0
    while True:
        players_online = get_current_players()
        if players_online>0:
            print(f"Countdown reset,{players_online} players online")
            countdown = 0
        else:
            print("No player online")
            countdown += 1

        if countdown >= 20:
            await channel.send("Server is closed due to inactivity") #  Sends message to channel
            print("Stopping server")
            stop()
            return

        sleep(60)



@client.event
async def on_ready():
    print("We have logged in as {0.user}" .format(client))

    channel = client.get_channel(976746947933257748) #  Gets channel from internal cache
    await count_down_loop(channel)
    # await channel.send("hello world") #  Sends message to channel


client.run(TOKEN)

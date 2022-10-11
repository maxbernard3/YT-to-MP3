# This is a terminal application
# no support for Linux
# you can download a playlist too, link should look like this: https://www.youtube.com/playlist?list=PLq-toGv_i0BA2iRkCZHjyu2zkOMte-blR

# need python 3

# need ffmpeg
# Windows : https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/
# MacOS : brew install ffmpeg (If you don't have hombrew, install it, it's good)

# need pytube : pip install pytube

import random
from pytube import YouTube
from pytube import Playlist
import os
from os import path
import json
from sys import platform
from pathlib import Path
import MacOS
import Windows
from Comon import remove

#need this to get appdata/local
user = os.getlogin()
global musicFolder
global APIkey
global pathLL


if (platform == 'Darwin' or platform == 'darwin'):
    pathLL = Path(f"/Users/{user}/AppData/Local/YTMP3/parameter.json")
    MacOS.createParam(user)

elif (platform == 'Windows' or platform == 'win32'):
    pathLL = Path(fr"C:/Users/{user}/AppData/LocalLow/YTMP3/parameter.json")
    Windows.createParam(user)

with open(pathLL, "r") as data:
    param = json.load(data)
    musicFolder = Path(param["filePath"])
    APIkey = param["apiKeys"]

# create a rapid api acount(s), get a 0$ plan at https://rapidapi.com/apidojo/api/shazam/pricing
# get the api key from https://rapidapi.com/developer/dashboard -> your default app -> security
# works with array so you can create many free acount

def main():
    with open(pathLL, "r") as data:
        param = json.load(data)
        musicFolder = Path(param["filePath"])
        APIkey = param["apiKeys"]
        if APIkey == [""]:
            print(
                "No API Key, type -A to add one\nGo on https://rapidapi.com/apidojo/api/shazam/pricing to get a free API key")

    l = input("help to see comand\n")

    if "help" in l:
        print("-A to add API keys \n-Y to enter YT link\n-T to change save path\n")
        main()
    elif '-A' in l:
        i = input("API key:\n")
        GetAPI(i)

    elif '-Y' in l:
        i = input("YT link:\n")
        if 'playlist' in i:
            GetYtPlay(i)
        else:
            high, yts = GetYtVid(i)
            if (platform == 'Darwin' or platform == 'darwin'):
                 MacOS.Download_and_sort(high, yts, musicFolder, APIkey)
            elif(platform == 'Windows' or platform == 'win32'):
                Windows.Download_and_sort(high, yts, musicFolder, APIkey)
        main()
    elif '-T' in l:
        i = input("new file Path:\n")
        ChangeTargetFile(i)
    else:
        print("invalid comand")
        main()




def GetYtVid(link):
    yt = YouTube(link)
    ys = yt.streams.filter(only_audio=True)

    highest = [None, 0]

    for i in range(len(ys)):
        if (int(ys[i].abr[:len(ys[i].abr) - 4]) > highest[1]):
            highest[1] = int(ys[i].abr[:len(ys[i].abr) - 4])
            highest[0] = ys[i]

    highest[0].download(musicFolder, "temp.webm")
    return (highest, yt)


def GetYtPlay(link):
    p = Playlist(link)
    i = 0
    for vid_url in p.video_urls:
        i += 1
        print(f"{i} in {len(p)}")
        high, yts = GetYtVid(vid_url)
        if (platform == 'Darwin' or platform == 'darwin'):
             MacOS.Download_and_sort(high, yts, musicFolder, APIkey)
        elif(platform == 'Windows' or platform == 'win32'):
            Windows.Download_and_sort(high, yts, musicFolder, APIkey)
    print("\n Done")


def GetAPI(key):
    param = ""
    with open(pathLL, "r") as data:
        param = json.load(data)

    with open(pathLL, "w") as FW:
        if param["apiKeys"] == [""]:
            param["apiKeys"] = [key]
            json.dump(param, FW)
        else:
            param["apiKeys"].append(key)
            json.dump(param, FW)

    print("Key added \n")
    main()


def ChangeTargetFile(target):
    with open(pathLL, "w") as FW:
        param["filePath"] = target
        json.dump(param, FW)
    musicFolder = target
    print("target path changed")
    main()


while (True):
    main()

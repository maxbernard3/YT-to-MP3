# This is a terminal application
# no support for Linux
# you can download a playlist too, link should look like this: https://www.youtube.com/playlist?list=PLq-toGv_i0BA2iRkCZHjyu2zkOMte-blR

# need python 3

# need ffmpeg
# Windows : https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/
# MacOS : brew install ffmpeg (If you don't have hombrew, install it, it's good)

# need pytube : pip install pytube

from pytube import YouTube
from pytube import Playlist
import os
import json
from sys import platform
from pathlib import Path
import MacOS
import Windows

# create a rapid api acount(s), get a 0$ plan at https://rapidapi.com/apidojo/api/shazam/pricing
# get the api key from https://rapidapi.com/developer/dashboard -> your default app -> security
# works with array so you can create many free acount

def main(musFolder, keys, pathLL):
    if keys == [""]:
        print(
            "No API Key, type -A to add one\nGo on https://rapidapi.com/apidojo/api/shazam/pricing to get a free API key")

    l = input("help to see comand\n")

    if "help" in l:
        print("\n-Y to enter YT link (autoclasificasion)\n-N to enter YT link (no clasificasion)\n-T to change save path\n-A to add API keys")
        main(GetParam()["filePath"], GetParam()["apiKeys"], pathLL)
    elif '-A' in l:
        i = input("API key:\n")
        GetAPI(i, pathLL)
        main(GetParam()["filePath"], GetParam()["apiKeys"], pathLL)
    elif '-Y' in l:
        getY(musFolder, keys)
        main(GetParam()["filePath"], GetParam()["apiKeys"], pathLL)
    elif '-T' in l:
        i = input("new file Path:\n")
        ChangeTargetFile(i, pathLL)
        main(GetParam()["filePath"], GetParam()["apiKeys"], pathLL)
    else:
        print("invalid comand")
        main(GetParam()["filePath"], GetParam()["apiKeys"], pathLL)


def GetParam():
    with open(getPathLL(), "r") as data:
        param = json.load(data)
    return param


def GetYtVid(link, musicFolder):
    yt = YouTube(link)
    ys = yt.streams.filter(only_audio=True)

    highest = [None, 0]

    for i in range(len(ys)):
        if (int(ys[i].abr[:len(ys[i].abr) - 4]) > highest[1]):
            highest[1] = int(ys[i].abr[:len(ys[i].abr) - 4])
            highest[0] = ys[i]

    highest[0].download(musicFolder, "temp.webm")
    return (highest, yt)


def GetYtPlay(link, musicFolder, APIkey):
    p = Playlist(link)
    i = 0
    for vid_url in p.video_urls:
        i += 1
        print(f"{i} in {len(p)}")
        high, yts = GetYtVid(vid_url, musicFolder)
        if (platform == 'Darwin' or platform == 'darwin'):
             MacOS.Download_and_sort(high, yts, musicFolder, APIkey)
        elif(platform == 'Windows' or platform == 'win32'):
            Windows.Download_and_sort(high, yts, musicFolder, APIkey)
    print("\n Done")


def getPathLL():
    user = os.getlogin()
    pathLL = ""
    if (platform == 'Darwin' or platform == 'darwin'):
        pathLL = Path(f"/Users/{user}/AppData/Local/YTMP3/parameter.json")
        MacOS.createParam(user)

    elif (platform == 'Windows' or platform == 'win32'):
        pathLL = Path(fr"C:/Users/{user}/AppData/LocalLow/YTMP3/parameter.json")
        Windows.createParam(user)
    return pathLL


def GetAPI(key, pathLL):
    param = GetParam()
    with open(pathLL, "w") as FW:
        if param["apiKeys"] == [""]:
            param["apiKeys"] = [key]
            json.dump(param, FW)
        else:
            param["apiKeys"].append(key)
            json.dump(param, FW)

    print("Key added \n")


def ChangeTargetFile(target, pathLL):
    param = GetParam()
    with open(pathLL, "w") as FW:
        param["filePath"] = target
        json.dump(param, FW)
    print("target path changed")

def getY(musicFolder, APIkey):
    if APIkey == [""]:
        print("no APIkey")
    else:
        i = input("YT link:\n")
        if 'playlist' in i:
            GetYtPlay(i, musicFolder, APIkey)
        else:
            high, yts = GetYtVid(i, musicFolder)
            if (platform == 'Darwin' or platform == 'darwin'):
                MacOS.Download_and_sort(high, yts, musicFolder, APIkey)
            elif (platform == 'Windows' or platform == 'win32'):
                Windows.Download_and_sort(high, yts, musicFolder, APIkey)


main(GetParam()["filePath"], GetParam()["apiKeys"], getPathLL())

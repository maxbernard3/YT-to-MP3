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
import argparse

if (platform == 'Darwin' or platform == 'darwin'):
     import MacOS as sysPlat
elif(platform == 'Windows' or platform == 'win32'):
    import Windows as sysPlat

# create a rapid api acount(s), get a 0$ plan at https://rapidapi.com/apidojo/api/shazam/pricing
# get the api key from https://rapidapi.com/developer/dashboard -> your default app -> security
# works with array so you can create many free acount

# Parser
parser = argparse.ArgumentParser(description='Run YT download and conversion')
parser.add_argument('-N', '--noclass', dest="no_class", help='download without clasification')
parser.add_argument('-Y', '--ytclass', dest="yt_class", help='download and clasify by artist')
parser.add_argument('-A', '--api', dest="apikey", help='add API key for autoclasification')
parser.add_argument('--rmapi', dest="rmapi", help='remove the last added API key')
parser.add_argument('-T', '--targetdir', dest="targetdir", help='change save path')

args = parser.parse_args()

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
        sysPlat.Download_and_sort(high, yts, musicFolder, APIkey)
    print("\n Done")

def GetYtPlayNoClasificasion(link, musicFolder):
    p = Playlist(link)
    i = 0
    for vid_url in p.video_urls:
        i += 1
        print(f"{i} in {len(p)}")
        high, yts = GetYtVid(vid_url, musicFolder)
        sysPlat.Download_no_sort(high, yts, musicFolder)
    print("\n Done")

def getPathLL():
    user = os.getlogin()
    return sysPlat.createParam(user)


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


def RemoveAPI(pathLL):
    param = GetParam()
    with open(pathLL, "w") as FW:
        if not param["apiKeys"] == [""]:
            if len(param["apiKeys"]) <= 1:
                param["apiKeys"] = [""]
            else:
                param["apiKeys"].pop()
            json.dump(param, FW)
            print("Key Removed\n")
        else:
            json.dump(param, FW)
            print("No API key to remove")

def ChangeTargetFile(target, pathLL):
    param = GetParam()
    with open(pathLL, "w") as FW:
        param["filePath"] = target
        json.dump(param, FW)
    print("target path changed")


def getY(i, musicFolder, APIkey):
    if APIkey == [""]:
        print("no APIkey so can't clasify")
    else:
        if 'playlist' in i:
            GetYtPlay(i, musicFolder, APIkey)
        else:
            high, yts = GetYtVid(i, musicFolder)
            sysPlat.Download_and_sort(high, yts, musicFolder, APIkey)


def getN(i, musicFolder):
    if 'playlist' in i:
        GetYtPlayNoClasificasion(i, musicFolder)
    else:
        high, yts = GetYtVid(i, musicFolder)
        sysPlat.Download_no_sort(high, yts, musicFolder)

if args.no_class:
    getN(args.no_class, GetParam()["filePath"])

if args.yt_class:
    getY(args.yt_class, GetParam()["filePath"], GetParam()["apiKeys"])

if args.apikey:
    GetAPI(GetParam()["apiKeys"], GetParam()["filePath"])

if args.apikey:
    GetAPI(args.apikey, GetParam()["filePath"])

if args.rmapi:
    RemoveAPI(GetParam()["filePath"])

if args.targetdir:
    ChangeTargetFile(args.targetdir, GetParam()["filePath"])
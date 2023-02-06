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
parser.add_argument('-N', '--noclass', dest='no_class', action='store_true',
                    help='download without clasification')
parser.add_argument('-C', '--ytclass', dest="yt_class", action="store_true",
                    help='download and clasify by artist')
parser.add_argument('-A', '--api', dest="apikey", action='store',
                    help='add API key for autoclasification', type=str)
parser.add_argument('-L', '--apilist', dest="apilist", action='store_true',
                    help='show all saved API key')
parser.add_argument('--rmapi', dest="rmapi", action='store_true',
                    help='remove the last added API key')
parser.add_argument('-T', '--targetdir', dest="targetdir", action='store',
                    help='change save path', type=str)

args = parser.parse_args()
if args.no_class and args.yt_class:
    raise ValueError('cant have both clasification and non classification')

pathLL = sysPlat.createParam()

def GetParam():
    with open(pathLL, "r") as data:
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

def GetAPI(key):
    param = GetParam()
    with open(pathLL, "w") as FW:
        if param["apiKeys"] == [""]:
            param["apiKeys"] = [key]
            json.dump(param, FW)
        else:
            param["apiKeys"].append(key)
            json.dump(param, FW)

    print("Key added")
    
def ListAPI():
    param = GetParam()
    for i in param["apiKeys"]:
        print(i)

def RemoveAPI():
    param = GetParam()
    with open(pathLL, "w") as FW:
        if not param["apiKeys"] == [""]:
            if len(param["apiKeys"]) <= 1:
                param["apiKeys"] = [""]
            else:
                param["apiKeys"].pop()
            json.dump(param, FW)
            print("Key Removed")
        else:
            json.dump(param, FW)
            print("No API key to remove")

def ChangeTargetFile(target):
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


if args.apikey:
    GetAPI(args.apikey)
    
if args.apilist:
    ListAPI()

if args.rmapi:
    RemoveAPI()

if args.targetdir:
    ChangeTargetFile(args.targetdir)
    
if args.no_class:
    A = True
    while A:
        print("type 'exit' to close the program")
        link = str(input("link: "))
        if link == "exit":
            A = False
        else:
            getN(link, GetParam()["filePath"])
            print("done")

if args.yt_class:
    A = True
    while A:
        print("type 'exit' to close the program")
        link = str(input("link: "))
        if link == "exit":
            A = False
        else:
            getY(link, GetParam()["filePath"], GetParam()["apiKeys"])
            print("done")
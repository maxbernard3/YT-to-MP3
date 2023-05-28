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
import json
from sys import platform
import argparse

if platform == 'Darwin' or platform == 'darwin':
    import MacOS as sysPlat
elif platform == 'Windows' or platform == 'win32':
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

pathLL = sysPlat.create_param()


def get_param():
    with open(pathLL, "r") as data:
        param = json.load(data)
    return param


def get_yt_vid(yt_link, music_folder):
    yt = YouTube(yt_link)
    ys = yt.streams.filter(only_audio=True)

    highest = [None, 0]

    for i in range(len(ys)):
        if (int(ys[i].abr[:len(ys[i].abr) - 4]) > highest[1]):
            highest[1] = int(ys[i].abr[:len(ys[i].abr) - 4])
            highest[0] = ys[i]

    highest[0].download(music_folder, "temp.webm")
    return (highest, yt)


def get_yt_playlist(link):
    sysPlat.check_0_remaining(get_param())

    p = Playlist(link)
    i = 0
    for vid_url in p.video_urls:
        param = get_param()
        i += 1
        print(f"{i} in {len(p)}")
        high, yts = get_yt_vid(vid_url, param["filePath"])
        catch = sysPlat.download_sort(high, yts, param)
        if catch:
            return
    print("\n Done")


def get_yt_playlist_no_classification(link, musicFolder):
    p = Playlist(link)
    i = 0
    for vid_url in p.video_urls:
        i += 1
        print(f"{i} in {len(p)}")
        high, yts = get_yt_vid(vid_url, musicFolder)
        sysPlat.download_no_sort(high, yts, musicFolder)
    print("\n Done")


def add_api_key(key):
    param = get_param()
    with open(pathLL, "w") as FW:
        if param["apiKeys"] == [""]:
            param["apiKeys"] = [key]
            param["remainingUses"] = [500]
            json.dump(param, FW)
        else:
            param["apiKeys"].append(key)
            param["remainingUses"].append(500)
            json.dump(param, FW)

    print("Key added")


def list_api_keys():
    sysPlat.check_0_remaining(get_param())
    param = get_param()
    for x, key in enumerate(param["apiKeys"]):
        print(f"{key}, remaining use {param['remainingUses'][x]}")


def remove_api_key():
    param = get_param()
    with open(pathLL, "w") as FW:
        if not param["apiKeys"] == [""]:
            if len(param["apiKeys"]) <= 1:
                param["apiKeys"] = [""]
                param["remainingUses"] = [0]
            else:
                param["apiKeys"].pop()
                param["remainingUses"].pop()
            json.dump(param, FW)
            print("Key Removed")
        else:
            json.dump(param, FW)
            print("No API key to remove")


def change_target_dir(target):
    param = get_param()
    with open(pathLL, "w") as FW:
        param["filePath"] = target
        json.dump(param, FW)
    print("target path changed")


def get_classification(i):
    sysPlat.check_0_remaining(get_param())

    param = get_param()
    if param["apiKeys"] == [""]:
        print("no APIkey so can't clasify")
    else:
        if 'playlist' in i:
            get_yt_playlist(i)
        else:
            high, yts = get_yt_vid(i, param["filePath"])
            catch = sysPlat.download_sort(high, yts, param)
            if catch:
                return True


def get_no_classification(i, music_folder):
    if 'playlist' in i:
        get_yt_playlist_no_classification(i, music_folder)
    else:
        high, yts = get_yt_vid(i, music_folder)
        sysPlat.download_no_sort(high, yts, music_folder)


# call functions from arg parse
if args.apikey:
    add_api_key(args.apikey)

if args.apilist:
    list_api_keys()

if args.rmapi:
    remove_api_key()

if args.targetdir:
    change_target_dir(args.targetdir)

if args.no_class:
    while True:
        print("type 'exit' to close the program")
        link = str(input("link: "))
        if link == "exit":
            break
        else:
            get_no_classification(link, get_param()["filePath"])
            print("done")

if args.yt_class:
    while True:
        print("type 'exit' to close the program")
        link = str(input("link: "))
        if link == "exit":
            break
        else:
            catch_ = get_classification(link)
            if catch_:
                break
            else:
                print("done")

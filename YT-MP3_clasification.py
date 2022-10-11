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
import base64
from sys import platform
from pathlib import Path

#need this to get appdata/local
user = os.getlogin()
global musicFolder
global APIkey
global pathLL


def createParamWin():
    musPath = (r"C:\\Users\\% s\\Music"%user)
    paramJson = '{"filePath": "% s","apiKeys": [""]}'%musPath

    if not path.exists(fr"C:\Users\{user}\AppData\LocalLow\YTMP3"):
        os.mkdir(fr"C:\Users\{user}\AppData\LocalLow\YTMP3")
        with open(fr"C:\Users\{user}\AppData\LocalLow\YTMP3\parameter.json", "w") as p:
            p.write(paramJson)

    else:
        if not path.exists(fr"C:\Users\{user}\AppData\LocalLow\YTMP3\parameter.json"):
            with open(fr"C:\Users\{user}\AppData\LocalLow\YTMP3\parameter.json", "w") as p:
                p.write(paramJson)


def createParamMac():
    musPath = "/Users/% s/Music" %user
    paramJson = '{"filePath": "% s","apiKeys": [""]}'%musPath

    if not path.exists(f"/Users/{user}/AppData/Local/YTMP3"):
        os.mkdir(f"/Users/{user}/AppData/Local/YTMP3")
        f = open(f"/Users/{user}/AppData/Local/YTMP3/parameter.json", "w")
        f.write(paramJson)
        f.close()
    else:
        if not path.exists(f"/Users/{user}/AppData/Local/YTMP3/parameter.json"):
            f = open(f"/Users/{user}/AppData/Local/YTMP3/parameter.json", "w")
            f.write(paramJson)
            f.close()


if (platform == 'Darwin' or platform == 'darwin'):
    import requests
    pathLL = Path(f"/Users/{user}/AppData/Local/YTMP3/parameter.json")
    createParamMac()

elif (platform == 'Windows' or platform == 'win32'):
    import http.client
    pathLL = Path(fr"C:/Users/{user}/AppData/LocalLow/YTMP3/parameter.json")
    createParamWin()

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
        i = input("API key:\n")
        GetAPI(i)

    elif '-Y' in l:
        i = input("YT link:\n")
        if 'playlist' in i:
            GetYtPlay(i)
        else:
            high, yts = GetYtVid(i)
            Download_and_sort(high, yts)
        main()
    elif '-T' in l:
        i = input("new file Path:\n")
        ChangeTargetFile(i)
    else:
        print("invalid comand")
        main()

def remove(string):
    b = r"!@#$/.()\'&"
    for char in b:
        string = string.replace(char, "")
    string = string.replace(" ", "-")

    return string


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
        Download_and_sort(high, yts)
    print("\n Done")


def Download_and_sort(highest, yt):
    track_title = f"{remove(yt.title)}"
    track_artist = f"NotFound"

    iter = 0

    while (iter < 5):
        if (platform == 'Darwin' or platform == 'darwin'):
            os.system(f"ffmpeg -i '{musicFolder}/temp.webm' -vn -ab 64k -ar 44100 -ss 00:00:{iter * 10} -ac 1 -fs 350000 -y '{musicFolder}/temp.wav'")

            f = open(f'{musicFolder}/temp.wav', 'rb')
            file_content = base64.b64encode(f.read())
            os.system(f"rm '{musicFolder}/temp.wav'")
            f.close()

            url = "https://shazam.p.rapidapi.com/songs/v2/detect"
            payload = file_content
            headers = {
                "content-type": "text/plain",
                f"X-RapidAPI-Key": str(APIkey[random.randint(0, len(APIkey) - 1)]),
                "X-RapidAPI-Host": "shazam.p.rapidapi.com"
            }

            response = requests.request("POST", url, data=payload, headers=headers)
            os.system("clear")

            json_data = json.loads(f"{response.text}")

            if (json_data['matches'] != []):
                track_title = remove(json_data['track']['title'])
                track_artist = remove(json_data['track']['subtitle'])
                iter = 6

            iter += 1

        elif (platform == 'Windows' or platform == 'win32'):
            os.system(fr"ffmpeg -i {musicFolder}\temp.webm -vn -ab 64k -ar 44100 -ss 00:00:{iter * 10} -ac 1 -fs 350000 -y {musicFolder}\temp.wav")

            f = open(fr'{musicFolder}\temp.wav', 'rb')
            file_content = base64.b64encode(f.read())
            f.close()

            conn = http.client.HTTPSConnection("shazam.p.rapidapi.com")
            payload = file_content
            headers = {
                "content-type": "text/plain",
                f"X-RapidAPI-Key": str(APIkey[random.randint(0, len(APIkey) - 1)]),
                "X-RapidAPI-Host": "shazam.p.rapidapi.com"
            }

            conn.request("POST", "/songs/v2/detect?timezone=America%2FChicago&locale=en-US", payload, headers)
            res = conn.getresponse()
            data = res.read()
            response = data.decode("utf-8")
            os.system("cls")

            json_data = json.loads(response)

            if (json_data['matches'] != []):
                track_title = remove(json_data['track']['title'])
                track_artist = remove(json_data['track']['subtitle'])
                iter = 6

            os.system(fr"del {musicFolder}\temp.wav")
            iter += 1

    if (platform == 'Darwin' or platform == 'darwin'):
        if (os.path.isdir(f"{musicFolder}/{track_artist}") == False):
            os.mkdir(f"{musicFolder}/{track_artist}")

        os.system(
            f"ffmpeg -i '{musicFolder}/temp.webm' -vn -ab {highest[1]}k -ar 44100 -y '{musicFolder}/{track_artist}/{track_title}.mp3'")
        os.system(f"rm '{musicFolder}/temp.webm'")
        os.system("clear")

    elif (platform == 'Windows' or platform == 'win32'):
        if (os.path.isdir(fr"{musicFolder}\{track_artist}") == False):
            os.mkdir(fr"{musicFolder}\{track_artist}")

        os.system(
            fr"ffmpeg -i {musicFolder}\temp.webm -vn -ab {highest[1]}k -ar 44100 -y {musicFolder}\{track_artist}\{track_title}.mp3")
        os.system(fr"del {musicFolder}\temp.webm")
        os.system("cls")


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

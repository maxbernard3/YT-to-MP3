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

#need this to get appdata/local
user = os.getlogin()
musicFolder = ""
APIkey = []
pathLL = ""

if (platform == 'Darwin' or platform == 'darwin'):
    import requests

elif (platform == 'Windows' or platform == 'win32'):
    import http.client
    pathLL = fr"C:\Users\{user}\AppData\LocalLow\YTMP3\parameter.json"

# create a rapid api acount(s), get a 0$ plan at https://rapidapi.com/apidojo/api/shazam/pricing
# get the api key from https://rapidapi.com/developer/dashboard -> your default app -> security
# works with array so you can create many free acount

def createParam():
    paramJson = "{\"filePath\":\"C:\\\\Users\\\\% s\\\\Music\",\"apiKeys\":[\"\"]}"% user
    if not path.exists(fr"C:\Users\{user}\AppData\LocalLow\YTMP3"):
        os.mkdir(fr"C:\Users\{user}\AppData\LocalLow\YTMP3")
        f = open(fr"C:\Users\{user}\AppData\LocalLow\YTMP3\parameter.json")
        f.write(paramJson)
        f.close()
    else:
        if not path.exists(fr"C:\Users\{user}\AppData\LocalLow\YTMP3\parameter.json"):
            f = open(fr"C:\Users\{user}\AppData\LocalLow\YTMP3\parameter.json", "w")
            f.write(paramJson)
            f.close()


createParam()
with open(pathLL, "r") as data:
    param = json.loads(data.read())
    musicFolder = param["filePath"]
    APIkey = param["apiKeys"]
    if APIkey == [""]:
        exit("No API key")

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


while (True):
    l = input("Enter YT link:")

    if 'playlist' in l:
        GetYtPlay(l)

    else:
        high, yts = GetYtVid(l)
        Download_and_sort(high, yts)

from os import path
from sys import platform
import os
import random
from Comon import remove
import json
import base64
import http.client

def createParam(user):
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


def Download_and_sort(highest, yt, musicFolder, APIkey):
    track_title = f"{remove(yt.title)}"
    track_artist = f"NotFound"

    iter = 0

    while (iter < 5):
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

        if (os.path.isdir(fr"{musicFolder}\{track_artist}") == False):
            os.mkdir(fr"{musicFolder}\{track_artist}")

        os.system(
            fr"ffmpeg -i {musicFolder}\temp.webm -vn -ab {highest[1]}k -ar 44100 -y {musicFolder}\{track_artist}\{track_title}.mp3")
        os.system(fr"del {musicFolder}\temp.webm")
        os.system("cls")

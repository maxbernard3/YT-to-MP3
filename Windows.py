from os import path
import os
import random
from Comon import remove
import json
import base64
from pathlib import Path
import http.client

def createParam():
    home = Path.home()
    musPath = f"{home}\Music".replace("\\", "\\\\")
    paramJson = '{"filePath": "% s","apiKeys": [""]}'%musPath

    if not path.exists(fr"{home}\AppData\LocalLow\YTMP3"):
        os.system(fr"mkdir {home}\AppData\LocalLow\YTMP3")
        with open(fr"{home}\AppData\LocalLow\YTMP3\parameter.json", "w") as p:
            p.write(paramJson)
    else:
        if not path.exists(fr"{home}\AppData\LocalLow\YTMP3\parameter.json"):
            with open(fr"{home}\AppData\LocalLow\YTMP3\parameter.json", "w") as p:
                p.write(paramJson)

    return Path(fr"{home}\AppData\LocalLow\YTMP3\parameter.json")

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

        json_data = json.loads(response)

        if (json_data['matches'] != []):
            track_title = remove(json_data['track']['title'])
            track_artist = remove(json_data['track']['subtitle'])
            iter = 6

        os.remove(f"{musicFolder}\\temp.wav")
        iter += 1

        if (os.path.isdir(fr"{musicFolder}\{track_artist}") == False):
            os.makedirs(fr"{musicFolder}\{track_artist}")

        os.system(
            fr"ffmpeg -i {musicFolder}\temp.webm -vn -ab {highest[1]}k -ar 44100 -y {musicFolder}\{track_artist}\{track_title}.mp3")
        os.remove(f"{musicFolder}\\temp.webm")


def Download_no_sort(highest, yt, musicFolder):
    track_title = f"{remove(yt.title)}"
    os.system(fr"ffmpeg -i {musicFolder}\temp.webm -vn -ab {highest[1]}k -ar 44100 -y {musicFolder}\{track_title}.mp3")
    os.remove(f"{musicFolder}\\temp.webm")

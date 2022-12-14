from os import path
import os
import random
from Comon import remove
import json
import base64
import requests

def createParam(user):
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


def Download_and_sort(highest, yt, musicFolder, APIkey):
    track_title = f"{remove(yt.title)}"
    track_artist = f"NotFound"

    iter = 0

    while (iter < 5):
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

    if (os.path.isdir(f"{musicFolder}/{track_artist}") == False):
        os.mkdir(f"{musicFolder}/{track_artist}")

    os.system(
        f"ffmpeg -i '{musicFolder}/temp.webm' -vn -ab {highest[1]}k -ar 44100 -y '{musicFolder}/{track_artist}/{track_title}.mp3'")
    os.system(f"rm '{musicFolder}/temp.webm'")
    os.system("clear")


def Download_no_sort(highest, yt, musicFolder):
    track_title = f"{remove(yt.title)}"
    os.system(f"ffmpeg -i '{musicFolder}/temp.webm' -vn -ab {highest[1]}k -ar 44100 -y '{musicFolder}/{track_title}.mp3'")
    os.system(f"rm '{musicFolder}/temp.webm'")
    os.system("clear")
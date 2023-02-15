from os import path
import os
from Comon import select_api
from Comon import remove
import json
import base64
from pathlib import Path
import http.client

def createParam():
    user = os.getlogin()
    musPath = (r"C:\\Users\\% s\\Music"%user)
    paramJson = '{"filePath": "% s","apiKeys": [""]}'%musPath

    if not path.exists(fr"C:\Users\{user}\AppData\LocalLow\YTMP3"):
        os.makedirs(fr"C:\Users\{user}\AppData\LocalLow\YTMP3")
        with open(fr"C:\Users\{user}\AppData\LocalLow\YTMP3\parameter.json", "w") as p:
            p.write(paramJson)

    else:
        if not path.exists(fr"C:\Users\{user}\AppData\LocalLow\YTMP3\parameter.json"):
            with open(fr"C:\Users\{user}\AppData\LocalLow\YTMP3\parameter.json", "w") as p:
                p.write(paramJson)

    return Path(fr"C:/Users/{user}/AppData/LocalLow/YTMP3/parameter.json")


def convert_to_base64(music_folder, iterator):
    os.system(
        fr"ffmpeg -i {music_folder}\temp.webm -vn -ab 64k -ar 44100 -ss 00:00:{iterator * 10} -ac 1 -fs 350000 -y {music_folder}\temp.wav")

    f = open(fr'{music_folder}\temp.wav', 'rb')
    file_content = base64.b64encode(f.read())
    f.close()

    return file_content


def question_api(file_content, apikey, remaining_use):
    index = select_api(remaining_use)

    conn = http.client.HTTPSConnection("shazam.p.rapidapi.com")
    payload = file_content
    headers = {
        "content-type": "text/plain",
        f"X-RapidAPI-Key": str(apikey[index]),
        "X-RapidAPI-Host": "shazam.p.rapidapi.com"
    }

    conn.request("POST", "/songs/v2/detect?timezone=America%2FChicago&locale=en-US", payload, headers)
    res = conn.getresponse()
    data = res.read()
    response = data.decode("utf-8")
    json_data = json.loads(response)

    return json_data

def Download_and_sort(highest, yt, param):
    musicFolder = param["filePath"]
    APIkey = param["apiKeys"]
    remaining_use = param["remainingUses"]

    track_title = f"{remove(yt.title)}"
    track_artist = f"NotFound"

    iterator = 0

    while (iterator < 5):
        file_content = convert_to_base64(musicFolder, iterator)
        json_data = question_api(file_content, APIkey, remaining_use)

        if (json_data['matches'] != []):
            track_title = remove(json_data['track']['title'])
            track_artist = remove(json_data['track']['subtitle'])
            iter = 6

        os.remove(f"{musicFolder}\temp.wav")
        iterator += 1

        if (os.path.isdir(fr"{musicFolder}\{track_artist}") == False):
            os.makedirs(fr"{musicFolder}\{track_artist}")

        os.system(
            fr"ffmpeg -i {musicFolder}\temp.webm -vn -ab {highest[1]}k -ar 44100 -y {musicFolder}\{track_artist}\{track_title}.mp3")
        os.remove(f"{musicFolder}\temp.webm")


def Download_no_sort(highest, yt, musicFolder):
    track_title = f"{remove(yt.title)}"
    os.system(fr"ffmpeg -i {musicFolder}\temp.webm -vn -ab {highest[1]}k -ar 44100 -y {musicFolder}\{track_title}.mp3")
    os.remove(f"{musicFolder}\temp.webm")

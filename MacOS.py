from os import path
import os
from Comon import remove
from Comon import select_api
import json
import base64
from pathlib import Path
import requests

def createParam():
    user = os.getlogin()
    musPath = "/Users/% s/Music" %user
    paramJson = '{"filePath": "% s","apiKeys": [""], "remainingUses": [0]}'%musPath

    if not path.exists(f"/Users/{user}/AppData/Local/YTMP3"):
        os.makedirs(f"/Users/{user}/AppData/Local/YTMP3")
        f = open(f"/Users/{user}/AppData/Local/YTMP3/parameter.json", "w")
        f.write(paramJson)
        f.close()
    else:
        if not path.exists(f"/Users/{user}/AppData/Local/YTMP3/parameter.json"):
            f = open(f"/Users/{user}/AppData/Local/YTMP3/parameter.json", "w")
            f.write(paramJson)
            f.close()

    return Path(f"/Users/{user}/AppData/Local/YTMP3/parameter.json")


def convert_to_base64(music_folder, iterator):
    os.system(
        f"ffmpeg -i '{music_folder}/temp.webm' -vn -ab 64k -ar 44100 -ss 00:00:{iterator * 10} -ac 1 -fs 350000 -y '{music_folder}/temp.wav'")

    f = open(f'{music_folder}/temp.wav', 'rb')
    file_content = base64.b64encode(f.read())
    os.remove(f"{music_folder}/temp.wav")
    f.close()
    return file_content


def question_api(file_content, apikey, remaining_use):
    index = select_api(remaining_use)

    url = "https://shazam.p.rapidapi.com/songs/v2/detect"
    payload = file_content
    headers = {
        "content-type": "text/plain",
        f"X-RapidAPI-Key": str(apikey[index]),
        "X-RapidAPI-Host": "shazam.p.rapidapi.com"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    json_data = json.loads(f"{response.text}")

    i_remaining_uses = (index, int(response.headers["X-RateLimit-Requests-Remaining"]))

    return json_data, i_remaining_uses


def Download_and_sort(highest, yt, param):
    musicFolder = param["filePath"]
    APIkey = param["apiKeys"]
    remaining_use = param["remainingUses"]

    track_title = f"{remove(yt.title)}"
    track_artist = f"NotFound"

    iterator = 0

    while iterator < 5:
        file_content = convert_to_base64(musicFolder, iterator)
        json_data, i_remaining_uses = question_api(file_content, APIkey, remaining_use)

        update_remaining(param, i_remaining_uses)
        
        if json_data['matches']:
            track_title = remove(json_data['track']['title'])
            track_artist = remove(json_data['track']['subtitle'])
            iterator = 6

        iterator += 1

    if not os.path.isdir(f"{musicFolder}/{track_artist}"):
        os.makedirs(f"{musicFolder}/{track_artist}")

    os.system(
        f"ffmpeg -i '{musicFolder}/temp.webm' -vn -ab {highest[1]}k -ar 44100 -y '{musicFolder}/{track_artist}/{track_title}.mp3'")
    os.remove(f"{musicFolder}/temp.webm")


def Download_no_sort(highest, yt, musicFolder):
    track_title = f"{remove(yt.title)}"
    os.system(f"ffmpeg -i '{musicFolder}/temp.webm' -vn -ab {highest[1]}k -ar 44100 -y '{musicFolder}/{track_title}.mp3'")
    os.remove(f"{musicFolder}/temp.webm")


def update_remaining(param, i_remaining):
    json_path = createParam()

    with open(json_path, "w") as FW:
        param["remainingUses"][i_remaining[0]] = i_remaining[1]
        json.dump(param, FW)

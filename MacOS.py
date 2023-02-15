from os import path
import os
import Comon
import json
import base64
from pathlib import Path
import requests


def create_param():
    user = os.getlogin()
    mus_path = "/Users/% s/Music" %user
    param_json = '{"filePath": "% s","apiKeys": [""], "remainingUses": [0]}'%mus_path

    if not path.exists(f"/Users/{user}/AppData/Local/YTMP3"):
        os.makedirs(f"/Users/{user}/AppData/Local/YTMP3")
        f = open(f"/Users/{user}/AppData/Local/YTMP3/parameter.json", "w")
        f.write(param_json)
        f.close()
    else:
        if not path.exists(f"/Users/{user}/AppData/Local/YTMP3/parameter.json"):
            f = open(f"/Users/{user}/AppData/Local/YTMP3/parameter.json", "w")
            f.write(param_json)
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
    index = Comon.select_api(remaining_use)

    if index == -1:
        return "", -1

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


def download_sort(highest, yt, param):
    music_folder = param["filePath"]
    ap_ikey = param["apiKeys"]
    remaining_use = param["remainingUses"]

    track_title = f"{Comon.remove(yt.title)}"
    track_artist = f"NotFound"

    iterator = 0

    while iterator < 5:
        file_content = convert_to_base64(music_folder, iterator)
        json_data, i_remaining_uses = question_api(file_content, ap_ikey, remaining_use)

        if i_remaining_uses == -1:
            os.remove(f"{music_folder}/temp.webm")
            print("\nAll API key have reached plan quota limits")
            return True

        update_remaining(param, i_remaining_uses)
        
        if json_data['matches']:
            track_title = Comon.remove(json_data['track']['title'])
            track_artist = Comon.remove(json_data['track']['subtitle'])
            iterator = 6

        iterator += 1

    if not os.path.isdir(f"{music_folder}/{track_artist}"):
        os.makedirs(f"{music_folder}/{track_artist}")

    os.system(
        f"ffmpeg -i '{music_folder}/temp.webm' -vn -ab {highest[1]}k -ar 44100 -y '{music_folder}/{track_artist}/{track_title}.mp3'")
    os.remove(f"{music_folder}/temp.webm")


def download_no_sort(highest, yt, musicFolder):
    track_title = f"{Comon.remove(yt.title)}"
    os.system(f"ffmpeg -i '{musicFolder}/temp.webm' -vn -ab {highest[1]}k -ar 44100 -y '{musicFolder}/{track_title}.mp3'")
    os.remove(f"{musicFolder}/temp.webm")


def update_remaining(param, i_remaining):
    json_path = create_param()

    with open(json_path, "w") as FW:
        param["remainingUses"][i_remaining[0]] = i_remaining[1]
        json.dump(param, FW)


def check_0_remaining(param):
    l0 = Comon.find_0_remaining(param["remainingUses"])
    payload = base64.b64encode(bytes("test_string", 'utf-8'))
    url = "https://shazam.p.rapidapi.com/songs/v2/detect"

    for i in l0:
        headers = {
            "content-type": "text/plain",
            f"X-RapidAPI-Key": str(param["apiKeys"][i]),
            "X-RapidAPI-Host": "shazam.p.rapidapi.com"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        rem = int(response.headers["X-RateLimit-Requests-Remaining"])
        i_remaining_uses = (i, rem)

        if not rem == param["remainingUses"][i]:
            update_remaining(param, i_remaining_uses)
from os import path
import os
import Comon
import json
import base64
from pathlib import Path
import requests


def create_param():
    home = Path.home()
    mus_path = fr"{home}\Music".replace("\\", "\\\\")
    param_json = '{"filePath": "% s","apiKeys": [""]}' % mus_path

    if not path.exists(fr"{home}\AppData\LocalLow\YTMP3"):
        os.makedirs(fr"{home}\AppData\LocalLow\YTMP3")
        with open(fr"{home}\AppData\LocalLow\YTMP3\parameter.json", "w") as p:
            p.write(param_json)

    else:
        if not path.exists(fr"{home}\AppData\LocalLow\YTMP3\parameter.json"):
            with open(fr"{home}\AppData\LocalLow\YTMP3\parameter.json", "w") as p:
                p.write(param_json)

    return Path(fr"{home}\AppData\LocalLow\YTMP3\parameter.json")


def convert_to_base64(music_folder, iterator):
    os.system(
        fr"ffmpeg -i {music_folder}\temp.webm -vn -ab 64k -ar 44100 -ss 00:00:{iterator * 10} -ac 1 -fs 350000 -y {music_folder}\temp.wav")

    f = open(fr'{music_folder}\\temp.wav', 'rb')
    file_content = base64.b64encode(f.read())
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
    api_key = param["apiKeys"]
    remaining_use = param["remainingUses"]

    track_title = f"{Comon.remove(yt.title)}"
    track_artist = f"NotFound"

    iterator = 0

    while iterator < 5:
        file_content = convert_to_base64(music_folder, iterator)
        json_data, i_remaining_uses = question_api(file_content, api_key, remaining_use)

        if i_remaining_uses == -1:
            os.remove(f"{music_folder}/temp.webm")
            print("\nAll API key have reached plan quota limits")
            return True

        update_remaining(param, i_remaining_uses)

        if json_data['matches']:
            track_title = Comon.remove(json_data['track']['title'])
            track_artist = Comon.remove(json_data['track']['subtitle'])
            iterator = 6

        os.remove(fr"{music_folder}\\temp.wav")
        iterator += 1

        if not os.path.isdir(fr"{music_folder}\{track_artist}"):
            os.makedirs(fr"{music_folder}\{track_artist}")

        os.system(
            fr"ffmpeg -i {music_folder}\temp.webm -vn -ab {highest[1]}k -ar 44100 -y {music_folder}\{track_artist}\{track_title}.mp3")
        os.remove(fr"{music_folder}\temp.webm")


def download_no_sort(highest, yt, music_folder):
    track_title = f"{Comon.remove(yt.title)}"
    os.system(fr"ffmpeg -i {music_folder}\temp.webm -vn -ab {highest[1]}k -ar 44100 -y {music_folder}\{track_title}.mp3")
    os.remove(fr"{music_folder}\temp.webm")


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

        if "X-RateLimit-Requests-Remaining" in response.headers:
            rem = int(response.headers["X-RateLimit-Requests-Remaining"])
            i_remaining_uses = (i, rem)

            if not rem == param["remainingUses"][i]:
                update_remaining(param, i_remaining_uses)
        else:
            update_remaining(param, (i, 0))
            print(f"{param['apiKeys'][i]} is not a valid API key")

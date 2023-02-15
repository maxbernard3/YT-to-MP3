from sys import platform
import unittest
import Main
import unittest
import os
from pathlib import Path


class TestMain(unittest.TestCase):
    def test_GetParam(self):
        if (platform == 'Darwin' or platform == 'darwin'):
            result = ('/Users' in Main.get_param()["filePath"])
            self.assertEqual(result, True)
        elif (platform == 'Windows' or platform == 'win32'):
            result = ('C:' in Main.get_param()["filePath"])
            self.assertEqual(result, True)

    def test_getPathLL(self):
        if (platform == 'Darwin' or platform == 'darwin'):
            self.assertEqual(Main.getPathLL(), Path(f"/Users/{os.getlogin()}/AppData/Local/YTMP3/parameter.json"))
        elif (platform == 'Windows' or platform == 'win32'):
            self.assertEqual(Main.getPathLL(), Path(fr"C:\Users\{os.getlogin()}\AppData\LocalLow\YTMP3\parameter.json"))

    def test_getVid(self):
        link = "https://music.youtube.com/watch?v=qkWosGPYOUI&list=RDAMVMqkWosGPYOUI"
        if (platform == 'Darwin' or platform == 'darwin'):
            Main.get_yt_vid(link, rf"/Users/{os.getlogin()}/Music")
            result = os.path.exists(rf"/Users/{os.getlogin()}/Music/temp.webm")
            self.assertEqual(result, True)
            os.remove(rf"/Users/{os.getlogin()}/Music/temp.webm")
        elif (platform == 'Windows' or platform == 'win32'):
            Main.get_yt_vid(link, rf"C:\Users\{os.getlogin()}\Music")
            result = os.path.exists(rf"C:\Users\{os.getlogin()}\Music\temp.webm")
            self.assertEqual(result, True)
            os.remove(rf"C:\Users\{os.getlogin()}\Music\temp.webm")

if __name__ == "__main__":
    unittest.main()

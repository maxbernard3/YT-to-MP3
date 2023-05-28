import sys
from pathlib import Path
import unittest
from os import path
sys.path.append("..")
import Main

Windows = False
MusPath = fr"{Path.home()}/Music"
if sys.platform == 'Windows' or sys.platform == 'win32':
    Windows = True
    MusPath = fr"{Path.home()}\Music".replace("\\", "\\\\")


class TestMain(unittest.TestCase):
    def test_get_param(self):
        param = Main.get_param()
        self.assertEqual(param["apiKeys"][0], "", 'get_param is broken')

    def test_add_api_key(self):
        Main.add_api_key("test")
        param = Main.get_param()
        self.assertEqual(param["apiKeys"][0], "test", 'get_param or add_api_key is broken')
        Main.remove_api_key()

    def test_remove_api_key(self):
        Main.add_api_key("test")
        Main.remove_api_key()
        param = Main.get_param()
        self.assertEqual(param["apiKeys"][0], "", 'get_param or remove_api_key is broken')

    def test_get_yt_vid(self):
        highest, yt = Main.get_yt_vid("https://music.youtube.com/watch?v=nNms5rOaGlk", MusPath)
        self.assertEqual(highest[1], 160, 'get_yt_vid got wrong high')

        if Windows:
            self.assertTrue(path.exists(fr"{MusPath}\\temp.webm"), "get_yt_vid did not create temp.webm")
        else:
            self.assertTrue(path.exists(fr"{MusPath}/temp.webm"), "get_yt_vid did not create temp.webm")

if __name__ == "__main__":
    unittest.main()

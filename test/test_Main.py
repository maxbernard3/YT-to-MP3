from sys import platform

import sys
sys.path.append("..")
import Main

import unittest
import os


class TestMain(unittest.TestCase):
    def test_GetParam(self):
        param = Main.GetParam()
        self.assertEqual(param["apiKeys"], "", 'getParam is broken')

        Main.GetAPI("test")

        self.assertEqual(param["apiKeys"], "test", 'getParam or getApi is broken')



if __name__ == "__main__":
    unittest.main()

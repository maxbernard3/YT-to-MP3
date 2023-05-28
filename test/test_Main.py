from sys import platform

import sys
sys.path.append("..")
import Main

import unittest
import os


class TestMain(unittest.TestCase):
    def test_GetParam(self):
        param = Main.GetParam()
        self.assertEqual(param["apiKeys"][0], "", 'getParam is broken')

        Main.GetAPI("test")
        
        param = Main.GetParam()
        self.assertEqual(param["apiKeys"][0], "test", 'getParam or getApi is broken')



if __name__ == "__main__":
    unittest.main()

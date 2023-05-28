import sys
sys.path.append("..")
import Main
import unittest


class TestMain(unittest.TestCase):
    def test_GetParam(self):
        param = Main.get_param()
        self.assertEqual(param["apiKeys"][0], "", 'getParam is broken')

        Main.add_api_key("test")
        
        param = Main.get_param()
        self.assertEqual(param["apiKeys"][0], "test", 'getParam or getApi is broken')


if __name__ == "__main__":
    unittest.main()

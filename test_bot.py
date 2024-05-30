# test_bot.py

import unittest
import os
import json
from bot import change_trade_link, save_trade_links, load_trade_links, TRADE_LINK_FILE

class TestBotFunctions(unittest.TestCase):
    def setUp(self):
        self.test_trade_links = {
            "user1": "https://steamcommunity.com/tradeoffer/new/?partner=user1&token=token1",
            "user2": "https://steamcommunity.com/tradeoffer/new/?partner=user2&token=token2"
        }
        save_trade_links(self.test_trade_links)

    def tearDown(self):
        if os.path.exists(TRADE_LINK_FILE):
            os.remove(TRADE_LINK_FILE)

    def test_change_trade_link(self):
        new_link = change_trade_link("user1")
        self.assertIsNotNone(new_link)
        self.assertTrue(new_link.startswith("https://steamcommunity.com/tradeoffer/new/"))

    def test_save_and_load_trade_links(self):
        save_trade_links(self.test_trade_links)
        loaded_links = load_trade_links()
        self.assertEqual(self.test_trade_links, loaded_links)

    def test_trade_link_persistence(self):
        # Change trade link and test persistence
        new_link = change_trade_link("user3")
        loaded_links = load_trade_links()
        self.assertEqual(new_link, loaded_links.get("user3"))

if __name__ == '__main__':
    unittest.main()

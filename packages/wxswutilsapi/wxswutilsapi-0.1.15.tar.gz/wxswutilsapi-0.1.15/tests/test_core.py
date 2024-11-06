# tests/test_core.py

import unittest
from wxswutilsapi import greet

class TestGreet(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("World"), "Hello, World!")

if __name__ == '__main__':
    unittest.main()

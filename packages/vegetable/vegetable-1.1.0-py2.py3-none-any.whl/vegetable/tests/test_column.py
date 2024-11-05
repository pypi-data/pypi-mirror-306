import unittest

from vegetable import *

class TestTableColumn(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tab = Table()
        cls.tab.column("Simple")

    def test_col_1(self):
        self.assertEqual(self.tab.columns[0].type, str)
        self.assertEqual(self.tab.columns[0].width, len("Simple"))



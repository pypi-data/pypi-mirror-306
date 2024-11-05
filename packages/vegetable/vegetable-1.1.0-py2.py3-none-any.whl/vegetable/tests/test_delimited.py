import unittest

from vegetable import Table
from vegetable.output.delimited import DelimitedOutput

class TestFormats(unittest.TestCase):
    def test_delimited(self):
        t = Table(
            output=DelimitedOutput(
                delimiter="|", 
                header=True, 
                strip=True, 
                escape="escape", 
                escape_char="\\", 
                record_separator="\n"
            )
        )
        t.column("Time of day")
        t.column("Meal")
        t.column("Rating out of 10")
        t.row(["morning", "elevensies", 10])
        t.row(["afternoon", "pre-tea", 10])
        t.row(["evening", "tea", 10])
        t.row(["night", "sleepysnack", 10])

        self.assertEqual(t.header_str(), "Time of day|Meal|Rating out of 10")
        self.assertEqual(t.separator_str(), "")
        self.assertEqual(t.mast_head(), "Time of day|Meal|Rating out of 10")
        self.assertEqual(t.row_str(["morning", "elevensies", 10]), "morning|elevensies|10")
        self.assertEqual(
            t.row_str({
                "Time of day": "morning", 
                "Meal": "elevensies", 
                "Rating out of 10": 10,
            }), 
            "morning|elevensies|10"
        )


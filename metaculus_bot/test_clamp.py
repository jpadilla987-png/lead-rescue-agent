import unittest

from metaculus_bot.bot import CappedTemplateBot


class BinaryClampTests(unittest.TestCase):
    def setUp(self):
        self.bot = CappedTemplateBot.__new__(CappedTemplateBot)

    def parse(self, text: str) -> float:
        return self.bot._extract_forecast_from_binary_rationale(
            text, max_prediction=1, min_prediction=0
        )

    def test_zero_becomes_one_percent(self):
        self.assertEqual(self.parse("Probability: 0%"), 0.01)

    def test_hundred_becomes_ninety_nine_percent(self):
        self.assertEqual(self.parse("Probability: 100%"), 0.99)

    def test_one_percent_stays_one_percent(self):
        self.assertEqual(self.parse("Probability: 1%"), 0.01)

    def test_ninety_nine_percent_stays_ninety_nine_percent(self):
        self.assertEqual(self.parse("Probability: 99%"), 0.99)

    def test_midrange_is_unchanged(self):
        self.assertEqual(self.parse("Probability: 63%"), 0.63)


if __name__ == "__main__":
    unittest.main()

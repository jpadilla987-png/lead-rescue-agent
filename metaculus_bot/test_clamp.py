import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from forecasting_tools import TemplateBot
from forecasting_tools.data_models.binary_report import BinaryPrediction


class BinaryProductionClampTests(unittest.TestCase):
    def setUp(self):
        self.bot = TemplateBot.__new__(TemplateBot)
        llm = AsyncMock()
        llm.invoke = AsyncMock(return_value="synthetic reasoning")
        self.bot.get_llm = lambda *args, **kwargs: llm
        self.bot._structure_output_validation_samples = 1

    def run_case(self, parsed_value: float) -> float:
        parsed = BinaryPrediction(prediction_in_decimal=parsed_value)
        target = (
            "forecasting_tools.forecast_bots.official_bots."
            "template_bot_2026_spring.structure_output"
        )
        with patch(target, new=AsyncMock(return_value=parsed)):
            result = asyncio.run(
                self.bot._binary_prompt_to_forecast(
                    question=type(
                        "Q",
                        (),
                        {"page_url": "https://example.invalid/question"},
                    )(),
                    prompt="synthetic prompt",
                )
            )
        return result.prediction_value

    def test_parser_zero_posts_one_percent(self):
        self.assertEqual(self.run_case(0.0), 0.01)

    def test_parser_one_posts_ninety_nine_percent(self):
        self.assertEqual(self.run_case(1.0), 0.99)

    def test_midrange_is_unchanged(self):
        self.assertEqual(self.run_case(0.63), 0.63)


if __name__ == "__main__":
    unittest.main()

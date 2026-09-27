from __future__ import annotations

import argparse
import asyncio
import os
import sys

from forecasting_tools import GeneralLlm, TemplateBot

FALL_TOURNAMENT = "fall-futureeval-2026"
MINIBENCH = "minibench"
FREE_MODEL = "openrouter/openrouter/free"


def build_bot(*, publish: bool) -> TemplateBot:
    free_llm = GeneralLlm(
        model=FREE_MODEL,
        temperature=0.2,
        timeout=90,
        allowed_tries=2,
    )
    return TemplateBot(
        research_reports_per_question=1,
        predictions_per_research_report=3,
        use_research_summary_to_forecast=False,
        publish_reports_to_metaculus=publish,
        folder_to_save_reports_to="metaculus_bot/logs",
        skip_previously_forecasted_questions=True,
        llms={
            "default": free_llm,
            "parser": free_llm,
            "summarizer": free_llm,
            "researcher": free_llm,
        },
    )


def secrets_ready() -> tuple[bool, list[str]]:
    missing = [
        name
        for name in ("METACULUS_TOKEN", "OPENROUTER_API_KEY")
        if not os.getenv(name)
    ]
    return (not missing, missing)


async def run(mode: str) -> int:
    ready, missing = secrets_ready()
    allow_post = os.getenv("ALLOW_METACULUS_POSTS", "").lower() == "true"

    if not ready:
        print("SAFE HOLD: missing required secrets: " + ", ".join(missing))
        print("No forecasts were posted.")
        return 0

    if not allow_post:
        print("SAFE HOLD: secrets exist but ALLOW_METACULUS_POSTS is not true.")
        print("No forecasts were posted.")
        return 0

    bot = build_bot(publish=True)

    targets = [FALL_TOURNAMENT]
    if mode == "all":
        targets.append(MINIBENCH)

    for tournament_id in targets:
        print(f"Forecasting tournament: {tournament_id}")
        await bot.forecast_on_tournament(tournament_id)

    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("fall", "all"),
        default="all",
        help="Forecast Fall 2026 only or Fall + current MiniBench.",
    )
    args = parser.parse_args()
    return asyncio.run(run(args.mode))


if __name__ == "__main__":
    sys.exit(main())

import asyncio
import logging
from datetime import datetime
from typing import Literal, Sequence

import typeguard

from forecasting_tools.forecasting.forecast_reports.binary_report import (
    BinaryReport,
)
from forecasting_tools.forecasting.forecast_reports.forecast_report import (
    ForecastReport,
)
from forecasting_tools.forecasting.forecast_team.forecast_team import (
    ForecastTeam,
)
from forecasting_tools.forecasting.metaculus_api import MetaculusApi
from forecasting_tools.forecasting.metaculus_question import (
    BinaryQuestion,
    MetaculusQuestion,
)

logger = logging.getLogger(__name__)


class TeamManager:

    def __init__(self, time_to_wait_between_questions: int = 0) -> None:
        self.time_to_wait_between_questions = time_to_wait_between_questions
        assert time_to_wait_between_questions >= 0

    async def run_and_publish_forecasts_on_all_open_questions(
        self, tournament_id: int
    ) -> list[ForecastReport]:
        reports = await self.run_forecasts_on_all_open_questions(tournament_id)
        await self.publish_forecasts(reports)
        return reports

    async def run_forecasts_on_all_open_questions(
        self, tournament_id: int
    ) -> list[ForecastReport]:
        questions = MetaculusApi.get_all_questions_from_tournament(
            tournament_id, filter_by_open=True
        )
        reports = await self.__run_forecast_on_questions(questions)
        return reports

    async def __run_forecast_on_questions(
        self, questions: Sequence[MetaculusQuestion]
    ) -> list[ForecastReport]:
        reports: list[ForecastReport] = []
        for question in questions:
            report = await ForecastTeam(question).run_forecast()
            reports.append(report)
            await asyncio.sleep(self.time_to_wait_between_questions)
        return reports

    async def publish_forecasts(
        self, reports: Sequence[ForecastReport]
    ) -> None:
        for report in reports:
            await report.publish_report_to_metaculus()

    async def benchmark_forecast_team(
        self, evaluation_depth: Literal["shallow", "medium", "deep"]
    ) -> float:
        """
        Below are the conclusions of a rough simulation of tournaments and skill levels
        to help with choosing sample sizes. See https://chatgpt.com/share/3fbc8106-829d-4fb3-a9e6-af0badf266df

        lower = decent but lower quality = 50% of my deviation values (prediction - community vote) is above ~0.25
        higher = decent but higher quality = 50% of my devaiation values (predition -community vote) is above ~0.17

        At 10 samples
        - 20% of being lower, but seeming higher
        - 40% chance of being lower but seeming higher

        At 20 samples
        - 5% of being lower, but seeming higher
        - 20% being higher, but seeming lower

        At 30 samples
        - 3% of being lower, but seeming higher
        - 10% of being higher, but seeming lower

        The chances for misidentification decreases as the bot gains a deviation distribution that leans more towards 0. The chances get higher as it leans more towars 1.
        """

        if evaluation_depth == "shallow":
            num_questions_to_benchmark_on = 10
        elif evaluation_depth == "medium":
            num_questions_to_benchmark_on = 20
        elif evaluation_depth == "deep":
            num_questions_to_benchmark_on = 30

        questions = MetaculusApi.get_benchmark_questions(
            num_questions_to_benchmark_on
        )
        assert len(questions) == num_questions_to_benchmark_on
        typeguard.check_type(questions, list[BinaryQuestion])
        reports = await self.__run_forecast_on_questions(questions)
        typeguard.check_type(reports, list[BinaryReport])
        average_deviation_score = BinaryReport.calculate_average_deviation_score(
            reports  # type: ignore
        )
        rounded_score = round(average_deviation_score, 4)
        file_path_to_save_reports = f"logs/forecasts/benchmarks/benchmark_reports__score_{rounded_score}__{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        BinaryReport.save_object_list_to_file_path(
            reports, file_path_to_save_reports
        )
        return average_deviation_score

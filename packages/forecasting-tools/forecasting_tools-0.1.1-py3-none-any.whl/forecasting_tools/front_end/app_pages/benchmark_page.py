import math
import os
import textwrap

import dotenv
import streamlit as st

from forecasting_tools.forecasting.forecast_reports.binary_report import (
    BinaryReport,
)
from forecasting_tools.front_end.helpers.app_page import AppPage
from forecasting_tools.front_end.helpers.custom_auth import CustomAuth
from forecasting_tools.front_end.helpers.general import footer, header
from forecasting_tools.front_end.helpers.report_displayer import (
    ReportDisplayer,
)


class BenchmarkPage(AppPage):
    FILE_PATH_IN_FRONT_END_FOLDER: str = "pages/benchmark_page.py"
    PAGE_DISPLAY_NAME: str = "📈  Benchmark"
    URL_PATH: str = "/benchmark"
    BENCHMARK_FILE_SELECTBOX_KEY: str = "benchmark_file_selectbox"

    @classmethod
    @CustomAuth.add_access_control()
    async def async_main(cls) -> None:
        header()
        st.title("Benchmarks")
        st.write("")
        benchmark_files = cls.__get_benchmark_files()
        selected_file = st.selectbox(
            "Select a benchmark file:",
            benchmark_files,
            key=cls.BENCHMARK_FILE_SELECTBOX_KEY,
        )

        if selected_file:
            reports = cls._load_benchmark_reports(selected_file)
            cls.__display_deviation_scores(reports)
            cls.__display_questions_and_forecasts(reports)
            cls.__display_deviation_score_simulation_results()
            ReportDisplayer.display_report_list(reports)
        footer()

    @staticmethod
    def __get_benchmark_files() -> list[str]:
        benchmark_dir = "front_end/mokoresearch_site/benchmarks"
        file_names = [
            f for f in os.listdir(benchmark_dir) if f.endswith(".json")
        ]
        file_names.sort(reverse=True)
        return file_names

    @staticmethod
    def _load_benchmark_reports(file_name: str) -> list[BinaryReport]:
        file_path = f"front_end/mokoresearch_site/benchmarks/{file_name}"
        return BinaryReport.convert_project_file_path_to_object_list(file_path)

    @classmethod
    def __display_deviation_scores(cls, reports: list[BinaryReport]) -> None:
        with st.expander("Deviation Scores of Benchmark", expanded=False):
            certain_reports = [
                r
                for r in reports
                if r.community_prediction is not None
                and (
                    r.community_prediction > 0.9
                    or r.community_prediction < 0.1
                )
            ]
            uncertain_reports = [
                r
                for r in reports
                if r.community_prediction is not None
                and 0.1 <= r.community_prediction <= 0.9
            ]
            cls.__display_stats_for_report_type(reports, "All Questions")
            cls.__display_stats_for_report_type(
                certain_reports,
                "Certain Questions: Community Prediction >90% or <10%",
            )
            cls.__display_stats_for_report_type(
                uncertain_reports,
                "Uncertain Questions: Community Prediction 10%-90%",
            )

    @classmethod
    def __display_stats_for_report_type(
        cls, reports: list[BinaryReport], title: str
    ) -> None:
        deviation_score = BinaryReport.calculate_average_deviation_score(
            reports
        )
        actual_deviation = math.sqrt(deviation_score)
        st.markdown(
            f"""
            #### {title}
            - Number of Questions: {len(reports)}
            - Deviation Score: {deviation_score:.4f}
            - Interpretation: On average, there is a {actual_deviation:.2%} difference between community and bot
            """
        )

    @classmethod
    def __display_questions_and_forecasts(
        cls, reports: list[BinaryReport]
    ) -> None:
        with st.expander("Questions and Forecasts", expanded=False):
            st.subheader("Question List")
            certain_reports = [
                r
                for r in reports
                if r.community_prediction is not None
                and (
                    r.community_prediction > 0.9
                    or r.community_prediction < 0.1
                )
            ]
            uncertain_reports = [
                r
                for r in reports
                if r.community_prediction is not None
                and 0.1 <= r.community_prediction <= 0.9
            ]

            cls.__display_question_stats_in_list(
                certain_reports,
                "Certain Questions (Community Prediction >90% or <10%)",
            )
            cls.__display_question_stats_in_list(
                uncertain_reports,
                "Uncertain Questions (Community Prediction 10%-90%)",
            )

    @classmethod
    def __display_question_stats_in_list(
        cls, report_list: list[BinaryReport], title: str
    ) -> None:
        st.subheader(title)
        sorted_reports = sorted(
            report_list,
            key=lambda r: (
                r.deviation_score if r.deviation_score is not None else -1
            ),
            reverse=True,
        )
        for report in sorted_reports:
            deviation = (
                report.deviation_score
                if report.deviation_score is not None
                else -1
            )
            st.write(
                f"- **Δ:** {deviation:.4f} | **🤖:** {report.prediction:.2%} | **👥:** {report.community_prediction:.2%} | **Question:** {report.question.question_text}"
            )

    @classmethod
    def __display_deviation_score_simulation_results(cls) -> None:
        text = textwrap.dedent(
            """
            Below is a simulation used to indicate that the deviation score function is maximized
            when brier/log score is maximized and give a general idea of what a good deviation score is.
            The deviation score function is defined as `deviation_score = abs(bot_forecast - community_forecast) ** 2`.
            The best score is 0, and the worst score is 1.

            The simulation was run with 100,000 questions with random probabilities for a variety of bot skill levels.
            We assume that the community prediction is the same as true probability.
            The bot's forecast was calculated using `bot_forecast = np.clip(np.random.normal(community_forecast, bot_skill), 0, 1)`.

            Bot Skill 0.01 (Very Good):
            - Average Brier Score: 0.1704
            - Average Log Score: 0.512
            - Average Deviation Score: 0.000099

            Bot Skill 0.05 (Good):
            - Average Brier Score: 0.1725
            - Average Log Score: 0.554
            - Average Deviation Score: 0.0024

            Bot Skill 0.1 (Medium):
            - Average Brier Score: 0.1788
            - Average Log Score: 0.691
            - Average Deviation Score: 0.0090

            Bot Skill 0.3 (Poor):
            - Average Brier Score: 0.2308
            - Average Log Score: 2.086
            - Average Deviation Score: 0.0617

            Bot Skill 0.5 (Very Poor):
            - Average Brier Score: 0.2918
            - Average Log Score: 4.568
            - Average Deviation Score: 0.1213

            Bot Skill 0.7 (Below Very Poor):
            - Average Brier Score: 0.3326
            - Average Log Score: 6.749
            - Average Deviation Score: 0.1641

            Bot Skill 0.9 (Even Worse):
            - Average Brier Score: 0.3661
            - Average Log Score: 8.602
            - Average Deviation Score: 0.1964

            Bot Skill 1.1 (Worse Still):
            - Average Brier Score: 0.3863
            - Average Log Score: 9.939
            - Average Deviation Score: 0.2171

            Bot Skill 1.3 (Very Bad):
            - Average Brier Score: 0.4026
            - Average Log Score: 10.929
            - Average Deviation Score: 0.2330

            Bot Skill 1.5 (Extremely Bad):
            - Average Brier Score: 0.4152
            - Average Log Score: 11.674
            - Average Deviation Score: 0.2441

            See https://chatgpt.com/share/4a5c7459-838f-4445-b3e0-32e645b91d16
            """
        )
        with st.expander("Deviation Score Simulation Results", expanded=False):
            st.markdown(text)


if __name__ == "__main__":
    dotenv.load_dotenv()
    BenchmarkPage.main()

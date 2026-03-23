from uuid import UUID
from typing import List, Dict
from datetime import datetime, timedelta

from ..interface_adapters import IEmotionRecordRepository


class TrendAnalysisResult:
    """Результат анализа трендов"""

    def __init__(
            self,
            average_mood: float,
            average_anxiety: float,
            average_fatigue: float,
            average_sleep: float,
            mood_trend: str,
            anxiety_trend: str,
            fatigue_trend: str,
            sleep_trend: str,
            recommendations: List[str]
    ):
        self.average_mood = average_mood
        self.average_anxiety = average_anxiety
        self.average_fatigue = average_fatigue
        self.average_sleep = average_sleep
        self.mood_trend = mood_trend
        self.anxiety_trend = anxiety_trend
        self.fatigue_trend = fatigue_trend
        self.sleep_trend = sleep_trend
        self.recommendations = recommendations


class AnalyzeTrendsUseCase:
    """Use Case: Анализ трендов эмоционального состояния"""

    def __init__(self, record_repo: IEmotionRecordRepository):
        self.record_repo = record_repo

    def execute(self, user_id: UUID, period_days: int = 30) -> TrendAnalysisResult:
        """
        Анализирует тренды эмоционального состояния

        Args:
            user_id: ID пользователя
            period_days: Период анализа в днях

        Returns:
            TrendAnalysisResult: Результаты анализа
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)

        records = self.record_repo.find_by_user_id(user_id, start_date, end_date)

        if not records:
            return TrendAnalysisResult(
                average_mood=0, average_anxiety=0, average_fatigue=0, average_sleep=0,
                mood_trend="нет данных", anxiety_trend="нет данных",
                fatigue_trend="нет данных", sleep_trend="нет данных",
                recommendations=["Заполните дневник эмоций для анализа"]
            )

        # Вычисляем средние значения
        avg_mood = sum(r.mood for r in records) / len(records)
        avg_anxiety = sum(r.anxiety for r in records) / len(records)
        avg_fatigue = sum(r.fatigue for r in records) / len(records)
        avg_sleep = sum(r.sleep_hours for r in records) / len(records)

        # Определяем тренды (сравниваем первую и последнюю недели)
        mid_point = len(records) // 2
        first_half = records[:mid_point]
        second_half = records[mid_point:] if mid_point > 0 else records

        def get_trend(first_avg: float, second_avg: float) -> str:
            if second_avg > first_avg + 0.5:
                return "улучшение"
            elif second_avg < first_avg - 0.5:
                return "ухудшение"
            else:
                return "стабильно"

        mood_trend = get_trend(
            sum(r.mood for r in first_half) / len(first_half),
            sum(r.mood for r in second_half) / len(second_half)
        )

        anxiety_trend = get_trend(
            sum(r.anxiety for r in first_half) / len(first_half),
            sum(r.anxiety for r in second_half) / len(second_half)
        )

        fatigue_trend = get_trend(
            sum(r.fatigue for r in first_half) / len(first_half),
            sum(r.fatigue for r in second_half) / len(second_half)
        )

        sleep_trend = get_trend(
            sum(r.sleep_hours for r in first_half) / len(first_half),
            sum(r.sleep_hours for r in second_half) / len(second_half)
        )

        # Генерируем рекомендации
        recommendations = []
        if avg_mood < 5:
            recommendations.append("Старайтесь отмечать позитивные моменты в течение дня")
        if avg_anxiety > 7:
            recommendations.append("Попробуйте практиковать дыхательные упражнения")
        if avg_fatigue > 7:
            recommendations.append("Обеспечьте себе больше времени для отдыха")
        if avg_sleep < 6:
            recommendations.append("Старайтесь ложиться спать раньше")

        return TrendAnalysisResult(
            average_mood=round(avg_mood, 1),
            average_anxiety=round(avg_anxiety, 1),
            average_fatigue=round(avg_fatigue, 1),
            average_sleep=round(avg_sleep, 1),
            mood_trend=mood_trend,
            anxiety_trend=anxiety_trend,
            fatigue_trend=fatigue_trend,
            sleep_trend=sleep_trend,
            recommendations=recommendations
        )
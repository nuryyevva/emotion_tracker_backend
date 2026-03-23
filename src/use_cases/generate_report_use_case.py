from uuid import UUID
from enum import Enum
from datetime import datetime, timedelta
from typing import List, Dict

from ..interface_adapters import IEmotionRecordRepository


class Period(Enum):
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class ChartType(Enum):
    LINE = "line"
    BAR = "bar"
    AREA = "area"


class Metric(Enum):
    MOOD = "mood"
    ANXIETY = "anxiety"
    FATIGUE = "fatigue"
    SLEEP = "sleep"


class Report:
    """Отчет"""

    def __init__(
            self,
            title: str,
            period: Period,
            charts: Dict[str, str],
            insights: List[str]
    ):
        self.title = title
        self.period = period
        self.charts = charts
        self.insights = insights


class GenerateReportUseCase:
    """Use Case: Генерация отчета"""

    def __init__(self, record_repo: IEmotionRecordRepository):
        self.record_repo = record_repo

    def execute(
            self,
            user_id: UUID,
            period: Period,
            chart_type: ChartType,
            metrics: List[Metric]
    ) -> Report:
        """
        Генерирует отчет

        Args:
            user_id: ID пользователя
            period: Период
            chart_type: Тип графика
            metrics: Метрики для включения

        Returns:
            Report: Сгенерированный отчет
        """
        # Определяем диапазон дат
        end_date = datetime.now()
        if period == Period.WEEK:
            start_date = end_date - timedelta(days=7)
            title = "Недельный отчет"
        elif period == Period.MONTH:
            start_date = end_date - timedelta(days=30)
            title = "Месячный отчет"
        else:
            start_date = end_date - timedelta(days=365)
            title = "Годовой отчет"

        records = self.record_repo.find_by_user_id(user_id, start_date, end_date)

        if not records:
            return Report(
                title=title,
                period=period,
                charts={},
                insights=["Нет данных за выбранный период"]
            )

        # Вычисляем инсайты
        insights = []
        avg_mood = sum(r.mood for r in records) / len(records)
        avg_anxiety = sum(r.anxiety for r in records) / len(records)
        avg_fatigue = sum(r.fatigue for r in records) / len(records)
        avg_sleep = sum(r.sleep_hours for r in records) / len(records)

        if avg_mood >= 7:
            insights.append("Общее настроение выше среднего")
        elif avg_mood <= 4:
            insights.append("Общее настроение ниже среднего")

        if avg_anxiety >= 7:
            insights.append("Уровень тревожности повышен")
        elif avg_anxiety <= 3:
            insights.append("Уровень тревожности низкий")

        if avg_sleep < 6:
            insights.append("Недостаток сна")

        # Заглушка для графиков
        charts = {m.value: f"Chart data for {m.value}" for m in metrics}

        return Report(
            title=title,
            period=period,
            charts=charts,
            insights=insights
        )
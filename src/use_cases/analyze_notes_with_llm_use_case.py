from uuid import UUID
from typing import List, Dict
from datetime import datetime, timedelta

from ..interface_adapters import IEmotionRecordRepository


class LLMSummary:
    """Сводка от LLM"""

    def __init__(
            self,
            summary: str,
            key_insights: List[str],
            recommendations: List[str]
    ):
        self.summary = summary
        self.key_insights = key_insights
        self.recommendations = recommendations


class AnalyzeNotesWithLLMUseCase:
    """Use Case: Анализ заметок с помощью LLM (заглушка)"""

    def __init__(self, record_repo: IEmotionRecordRepository):
        self.record_repo = record_repo

    def execute(self, user_id: UUID, period_days: int = 30) -> LLMSummary:
        """
        Анализирует заметки с помощью LLM

        Args:
            user_id: ID пользователя
            period_days: Период в днях

        Returns:
            LLMSummary: Сводка анализа
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)

        records = self.record_repo.find_by_user_id(user_id, start_date, end_date)

        # Фильтруем записи с заметками
        notes = [r.note for r in records if r.note]

        if not notes:
            return LLMSummary(
                summary="Нет заметок для анализа",
                key_insights=["Добавьте заметки для более глубокого анализа"],
                recommendations=["Пишите заметки каждый день"]
            )

        # Заглушка для LLM
        return LLMSummary(
            summary=f"Проанализировано {len(notes)} заметок за {period_days} дней",
            key_insights=[
                "Заметки содержат упоминания о работе",
                "Часто встречаются темы стресса и отдыха"
            ],
            recommendations=[
                "Старайтесь писать больше позитивных заметок",
                "Отмечайте достижения и успехи"
            ]
        )

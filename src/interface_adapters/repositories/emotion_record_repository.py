from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from ...entities.emotion_record import EmotionRecord


class IEmotionRecordRepository(ABC):
    """Интерфейс репозитория записей эмоций"""

    @abstractmethod
    def save(self, record: EmotionRecord) -> EmotionRecord:
        """Сохраняет запись"""
        pass

    @abstractmethod
    def find_by_user_id(
            self,
            user_id: UUID,
            start_date: datetime,
            end_date: datetime
    ) -> List[EmotionRecord]:
        """Находит записи пользователя за период"""
        pass

    @abstractmethod
    def find_latest_by_user_id(
            self,
            user_id: UUID,
            limit: int = 10
    ) -> List[EmotionRecord]:
        """Находит последние записи пользователя"""
        pass

    @abstractmethod
    def find_consecutive_days(
            self,
            user_id: UUID,
            metric: str,
            threshold: int,
            n_days: int
    ) -> bool:
        """Проверяет, были ли n дней подряд с метрикой выше порога"""
        pass

    @abstractmethod
    def find_today_record(self, user_id: UUID) -> Optional[EmotionRecord]:
        """Находит запись за сегодня"""
        pass
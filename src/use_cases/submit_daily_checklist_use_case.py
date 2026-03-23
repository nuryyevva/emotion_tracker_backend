from uuid import UUID
from typing import Optional
from datetime import datetime

from ..entities import EmotionRecord
from ..interface_adapters import IEmotionRecordRepository


class SubmitDailyChecklistUseCase:
    """Use Case: Отправка ежедневного чекапа эмоций"""

    def __init__(self, record_repo: IEmotionRecordRepository):
        self.record_repo = record_repo

    def execute(
            self,
            user_id: UUID,
            mood: int,
            anxiety: int,
            fatigue: int,
            sleep_hours: float,
            note: Optional[str] = None
    ) -> EmotionRecord:
        """
        Создает новую запись эмоционального состояния

        Args:
            user_id: ID пользователя
            mood: Настроение (1-10)
            anxiety: Тревожность (1-10)
            fatigue: Усталость (1-10)
            sleep_hours: Часы сна
            note: Заметка (необязательно)

        Returns:
            EmotionRecord: Созданная запись

        Raises:
            ValueError: Если данные невалидны
        """
        # Проверяем, нет ли уже записи за сегодня
        today_record = self.record_repo.find_today_record(user_id)
        if today_record:
            raise ValueError("Запись за сегодня уже существует")

        # Создаем запись
        record = EmotionRecord.create(
            user_id=user_id,
            mood=mood,
            anxiety=anxiety,
            fatigue=fatigue,
            sleep_hours=sleep_hours,
            note=note
        )

        # Сохраняем
        saved_record = self.record_repo.save(record)

        return saved_record
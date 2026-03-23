from uuid import UUID
from typing import List
from datetime import datetime

from ..entities import EmotionRecord
from ..interface_adapters import IEmotionRecordRepository


class GetEmotionHistoryUseCase:
    """Use Case: Получение истории эмоций"""

    def __init__(self, record_repo: IEmotionRecordRepository):
        self.record_repo = record_repo

    def execute(
            self,
            user_id: UUID,
            start_date: datetime,
            end_date: datetime
    ) -> List[EmotionRecord]:
        """
        Возвращает историю эмоций за указанный период

        Args:
            user_id: ID пользователя
            start_date: Начальная дата
            end_date: Конечная дата

        Returns:
            List[EmotionRecord]: Список записей
        """
        return self.record_repo.find_by_user_id(user_id, start_date, end_date)
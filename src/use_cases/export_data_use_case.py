from uuid import UUID
from enum import Enum
from datetime import datetime, timedelta
from typing import List

from ..interface_adapters import IEmotionRecordRepository


class ExportFormat(Enum):
    CSV = "csv"
    PDF = "pdf"
    JSON = "json"


class ExportDataUseCase:
    """Use Case: Экспорт данных пользователя"""

    def __init__(self, record_repo: IEmotionRecordRepository):
        self.record_repo = record_repo

    def execute(
            self,
            user_id: UUID,
            period_days: int,
            format: ExportFormat
    ) -> str:
        """
        Экспортирует данные пользователя

        Args:
            user_id: ID пользователя
            period_days: Период в днях
            format: Формат экспорта

        Returns:
            str: Строка с экспортированными данными
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)

        records = self.record_repo.find_by_user_id(user_id, start_date, end_date)

        if format == ExportFormat.JSON:
            return self._export_json(records)
        elif format == ExportFormat.CSV:
            return self._export_csv(records)
        else:
            return self._export_pdf(records)

    def _export_json(self, records: List) -> str:
        """Экспорт в JSON"""
        import json
        data = [
            {
                "date": r.date.isoformat(),
                "mood": r.mood,
                "anxiety": r.anxiety,
                "fatigue": r.fatigue,
                "sleep_hours": r.sleep_hours,
                "note": r.note
            }
            for r in records
        ]
        return json.dumps(data, ensure_ascii=False, indent=2)

    def _export_csv(self, records: List) -> str:
        """Экспорт в CSV"""
        lines = ["date,mood,anxiety,fatigue,sleep_hours,note"]
        for r in records:
            line = f"{r.date.isoformat()},{r.mood},{r.anxiety},{r.fatigue},{r.sleep_hours},{r.note or ''}"
            lines.append(line)
        return "\n".join(lines)

    def _export_pdf(self, records: List) -> str:
        """Экспорт в PDF (заглушка)"""
        return f"PDF export for {len(records)} records (не реализовано)"
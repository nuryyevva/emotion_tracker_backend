from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Union
from uuid import UUID, uuid4
import re

@dataclass
class EmotionRecord:
    user_id: UUID
    mood: int
    anxiety: int
    fatigue: int
    sleep_hours: float
    date: datetime = field(default_factory=datetime.now)
    note: Optional[str] = None
    id: UUID = field(default_factory=uuid4)

    @classmethod
    def create(
            cls,
            user_id: UUID,
            mood: int,
            anxiety: int,
            fatigue: int,
            sleep_hours: float,
            note: Optional[str] = None
    ) -> 'EmotionRecord':

        record = cls(
            user_id=user_id,
            mood=mood,
            anxiety=anxiety,
            fatigue=fatigue,
            sleep_hours=sleep_hours,
            note=note
        )

        if not record.validate():
            raise ValueError("Invalid data in the record")

        return record

    def validate(self) -> bool:
        if not all(1 <= x <= 10 for x in [self.mood, self.anxiety, self.fatigue]):
            return False

        if self.note and len(self.note) > 500:
            return False

        if self.sleep_hours < 0:
            return False

        return True

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class EmotionRecord:
    id: UUID
    user_id: UUID
    mood: int
    anxiety: int
    fatigue: int
    sleep_hours: float
    date: datetime
    note: Optional[str] = None

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
            id=uuid4(),
            user_id=user_id,
            mood=mood,
            anxiety=anxiety,
            fatigue=fatigue,
            sleep_hours=sleep_hours,
            date=datetime.now,
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

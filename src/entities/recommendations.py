from dataclasses import dataclass, field
from uuid import UUID, uuid4

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .emotion_record import EmotionRecord


@dataclass
class Recommendation:
    id: UUID = field(default_factory=uuid4)
    trigger_type: str = ""
    category: str = ""
    message: str = ""
    priority: int = 1

    @classmethod
    def create(
            cls,
            trigger_type: str,
            category: str,
            message: str,
            priority: int
    ) -> 'Recommendation':

        if priority < 1 or priority > 5:
            raise ValueError("Priority must be from 1 to 5")

        valid_trigger_types = ["fatigue_high", "anxiety_high", "mood_low", "sleep_low"]
        valid_categories = ["дыхание", "движение", "микро-действие", "отдых"]

        if trigger_type not in valid_trigger_types:
            raise ValueError(f"Wrong trigger type. Valid trigger types: {valid_trigger_types}")

        if category not in valid_categories:
            raise ValueError(f"Wrong category. Valid categories: {valid_categories}")

        return cls(
            trigger_type=trigger_type,
            category=category,
            message=message,
            priority=priority
        )

    def is_applicable(self, emotion_record: 'EmotionRecord') -> bool:
        from .emotion_record import EmotionRecord

        if not isinstance(emotion_record, EmotionRecord):
            return False

        if self.trigger_type == "fatigue_high" and emotion_record.fatigue >= 8:
            return True
        elif self.trigger_type == "anxiety_high" and emotion_record.anxiety >= 8:
            return True
        elif self.trigger_type == "mood_low" and emotion_record.mood <= 3:
            return True
        elif self.trigger_type == "sleep_low" and emotion_record.sleep_hours < 6:
            return True

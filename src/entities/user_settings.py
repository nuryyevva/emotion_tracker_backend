from typing import Optional, List
from uuid import UUID
from datetime import time
from dataclasses import dataclass


@dataclass
class SleepSchedule:
    weekday_wake_up: time
    weekday_bedtime: time
    weekend_wake_up: time
    weekend_bedtime: time

    def __post_init__(self):
        self.validate()

    def validate(self) -> bool:
        if self.weekday_wake_up == self.weekday_bedtime:
            raise ValueError("Weekday wake up must not be equal bedtime")
        if self.weekend_wake_up == self.weekend_bedtime:
            raise ValueError("Weekend wake up must not be equal bedtime")
        return True


@dataclass
class NotificationPreferences:
    channel: str  # "telegram" or "email"
    time_window_start: time
    time_window_end: time
    frequency: str  # "daily", "weekly"

    def __post_init__(self):
        self.validate()

    def validate(self) -> bool:
        valid_channels = ["telegram", "email"]
        valid_frequencies = ["daily", "weekly"]

        if self.channel not in valid_channels:
            raise ValueError(f"The channel must be one of: {valid_channels}")

        if self.frequency not in valid_frequencies:
            raise ValueError(f"The frequency must be one of: {valid_frequencies}")

        if self.time_window_start >= self.time_window_end:
            raise ValueError("Time window start must be earlier than time window end")

        return True


@dataclass
class UserSettings:
    """Настройки пользователя - только данные для хранения"""
    user_id: UUID
    hobbies: List[str]
    stress_coping_methods: List[str]
    sleep_schedule: Optional[SleepSchedule]
    notification_prefs: Optional[NotificationPreferences]

    @classmethod
    def create(cls, user_id: UUID) -> 'UserSettings':
        """Создание настроек по умолчанию"""
        default_sleep = SleepSchedule(
            weekday_wake_up=time(7, 0),
            weekday_bedtime=time(23, 0),
            weekend_wake_up=time(9, 0),
            weekend_bedtime=time(0, 0)
        )

        default_notifications = NotificationPreferences(
            channel="email",
            time_window_start=time(9, 0),
            time_window_end=time(21, 0),
            frequency="daily"
        )

        return cls(
            user_id=user_id,
            hobbies=[],
            stress_coping_methods=[],
            sleep_schedule=default_sleep,
            notification_prefs=default_notifications
        )

    def add_hobby(self, hobby: str) -> None:
        if hobby not in self.hobbies:
            self.hobbies.append(hobby)

    def remove_hobby(self, hobby: str) -> None:
        if hobby in self.hobbies:
            self.hobbies.remove(hobby)

    def add_stress_coping_method(self, method: str) -> None:
        if method not in self.stress_coping_methods:
            self.stress_coping_methods.append(method)

    def remove_stress_coping_method(self, method: str) -> None:
        if method in self.stress_coping_methods:
            self.stress_coping_methods.remove(method)

    def update_sleep_schedule(self, schedule: SleepSchedule) -> None:
        self.sleep_schedule = schedule

    def update_notification_preferences(self, prefs: NotificationPreferences) -> None:
        self.notification_prefs = prefs

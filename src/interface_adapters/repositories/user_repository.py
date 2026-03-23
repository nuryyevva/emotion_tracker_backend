from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from ...entities import User, UserSettings


class IUserRepository(ABC):
    """Интерфейс репозитория пользователей"""

    @abstractmethod
    def save(self, user: User) -> User:
        """Сохраняет пользователя"""
        pass

    @abstractmethod
    def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Находит пользователя по ID"""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """Находит пользователя по email"""
        pass

    @abstractmethod
    def update_settings(self, user_id: UUID, settings: UserSettings) -> None:
        """Обновляет настройки пользователя"""
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> bool:
        """Удаляет пользователя"""
        pass
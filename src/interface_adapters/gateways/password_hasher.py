from abc import ABC, abstractmethod


class IPasswordHasher(ABC):
    """Интерфейс для хеширования паролей"""

    @abstractmethod
    def hash(self, password: str) -> str:
        """Хеширует пароль"""
        pass

    @abstractmethod
    def verify(self, password: str, password_hash: str) -> bool:
        """Проверяет пароль"""
        pass
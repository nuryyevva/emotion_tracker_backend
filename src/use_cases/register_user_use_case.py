from typing import Optional
from uuid import UUID

from ..entities import User
from ..interface_adapters import IUserRepository, IPasswordHasher


class RegisterUserUseCase:
    """Use Case: Регистрация нового пользователя"""

    def __init__(self, user_repo: IUserRepository, password_hasher: IPasswordHasher):
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    def execute(self, email: str, password: str, timezone: str) -> User:
        """
        Регистрирует нового пользователя

        Args:
            email: Email пользователя
            password: Пароль
            timezone: Часовой пояс

        Returns:
            User: Созданный пользователь

        Raises:
            ValueError: Если email уже существует или данные невалидны
        """
        # Проверяем, не существует ли уже пользователь с таким email
        existing_user = self.user_repo.find_by_email(email)
        if existing_user:
            raise ValueError("Пользователь с таким email уже существует")

        # Валидируем email
        if not User.validate_email(email):
            raise ValueError("Некорректный email адрес")

        # Хешируем пароль
        password_hash = self.password_hasher.hash(password)

        # Создаем пользователя
        user = User.create(email, password_hash, timezone)

        # Сохраняем в репозиторий
        saved_user = self.user_repo.save(user)

        return saved_user
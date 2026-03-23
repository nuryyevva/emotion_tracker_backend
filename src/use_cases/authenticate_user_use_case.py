from typing import Optional

from ..entities import User
from ..interface_adapters import IUserRepository, IPasswordHasher


class AuthenticateUserUseCase:
    """Use Case: Аутентификация пользователя"""

    def __init__(self, user_repo: IUserRepository, password_hasher: IPasswordHasher):
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    def execute(self, email: str, password: str) -> Optional[User]:
        """
        Аутентифицирует пользователя

        Args:
            email: Email пользователя
            password: Пароль

        Returns:
            User | None: Пользователь если аутентификация успешна, иначе None
        """
        # Находим пользователя по email
        user = self.user_repo.find_by_email(email)

        if not user:
            return None

        # Проверяем пароль
        if not self.password_hasher.verify(password, user.password_hash):
            return None

        return user
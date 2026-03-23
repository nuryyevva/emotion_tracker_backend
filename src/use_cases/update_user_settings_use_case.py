from uuid import UUID

from ..entities import UserSettings
from ..interface_adapters import IUserRepository


class UpdateUserSettingsUseCase:
    """Use Case: Обновление настроек пользователя"""

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: UUID, settings: UserSettings) -> UserSettings:
        """
        Обновляет настройки пользователя

        Args:
            user_id: ID пользователя
            settings: Новые настройки

        Returns:
            UserSettings: Обновленные настройки

        Raises:
            ValueError: Если пользователь не найден
        """
        # Проверяем существование пользователя
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")

        # Обновляем настройки
        self.user_repo.update_settings(user_id, settings)

        return settings

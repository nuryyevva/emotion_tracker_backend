from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Union
from uuid import UUID, uuid4
import re
import bcrypt


@dataclass
class User:
    email: str
    password_hash: str
    timezone: str
    created_at: datetime = field(default_factory=datetime.now)
    id: UUID = field(default_factory=uuid4)

    @classmethod
    def create(cls, email: str, password: str, timezone: str) -> 'User':
        if not cls.validate_email(email):
            raise ValueError("Uncorrect email address")

        password_hash = cls._hash_password(password)

        return cls(
            email=email,
            password_hash=password_hash,
            timezone=timezone
        )

    def update_settings(self, settings: 'UserSettings') -> None:
        # changes in databases
        pass

    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt(rounds=12)
        ).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def change_password(self, old_password: str, new_password: str) -> bool:
        if not self.check_password(old_password):
            return False

        self.password_hash = self._hash_password(new_password)
        return True
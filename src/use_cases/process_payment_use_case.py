from uuid import UUID
from decimal import Decimal
from typing import Optional


class SubscriptionPlan:
    """План подписки"""
    FREE = "free"
    PREMIUM = "premium"
    PRO = "pro"


class PaymentResult:
    """Результат платежа"""

    def __init__(self, success: bool, transaction_id: Optional[str] = None):
        self.success = success
        self.transaction_id = transaction_id


class ProcessPaymentUseCase:
    pass

from datetime import datetime
from typing import Literal
from uuid import uuid4

from app.domain.value_objects.money import Money


class Transaction:
    """Aggregate root for transaction"""

    STATUS_PENDING = "pending"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"

    def __init__(
        self,
        from_account: str | None,
        to_account: str | None,
        amount: Money,
        status: Literal[STATUS_PENDING, STATUS_COMPLETED, STATUS_FAILED] = STATUS_PENDING,
        timestamp: datetime = None,
        pk: str = None
    ):
        self.pk = pk or str(uuid4())
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount
        self.status = status
        self.timestamp = timestamp or datetime.now()

    def mark_as_completed(self):
        """Mark the transaction as completed"""
        self.status = self.STATUS_COMPLETED

    def mark_as_failed(self):
        """Mark the transaction as failed"""
        self.status = self.STATUS_FAILED

    def mark_as_pending(self):
        """Mark the transaction as pending"""
        self.status = self.STATUS_PENDING
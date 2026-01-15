from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from app.domain.value_objects.money import Money


class TransactionStatus(str, Enum):
    """Status of a transaction"""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Transaction(BaseModel):
    """Represents a transfer between accounts."""

    pk: str = Field(..., description="The primary key of the transaction")
    from_account: str = Field(..., description="Source account PK")
    to_account: str = Field(..., description="Destination account PK")
    amount: Money = Field(..., description="Amount being transferred")
    timestamp: datetime = Field(default_factory=datetime.now)
    status: TransactionStatus = Field(default=TransactionStatus.PENDING, description="Status of the transaction")
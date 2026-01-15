from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.value_objects.money import Money


class Account(BaseModel):
    """Aggregate root representing a bank account"""

    pk: str = Field(..., description="The primary key of the account")
    owner: str = Field(..., description="The owner of the account or ID")
    balance: Money = Field(..., description="Current balance of the account")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency ISO code")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def deposit(self, amount: Money) -> None:
        """Deposit money into the account"""
        if amount.currency != self.currency:
            raise ValueError("Cannot deposit money with different currencies")
        self.balance += amount
        self.updated_at = datetime.now()

    def withdraw(self, amount: Money) -> None:
        """Withdraw money from the account"""
        if amount.currency != self.currency:
            raise ValueError("Currency mismatch")
        if self.balance.amount < amount.amount:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.updated_at = datetime.now()

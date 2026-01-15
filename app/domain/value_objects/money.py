from decimal import ROUND_HALF_UP, Decimal
from typing import Any


class Money:
    """Value object for money"""
    def __init__(self, amount: Decimal, currency: str = "USD"):
        self.amount = Decimal(amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.currency = currency

    def __add__(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, multiplier: float) -> "Money":
        return Money(self.amount * Decimal(multiplier), self.currency)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount and self.currency == other.currency

    def _check_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError(f"Cannot perform operation on different currencies: \
            {self.currency} and {other.currency}")

    def __repr__(self) -> str:
        return f"Money(amount={self.amount}, currency='{self.currency}')"

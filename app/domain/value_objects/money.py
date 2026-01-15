from pydantic import BaseModel, Field, condecimal


class Money(BaseModel):
    """Immutable value object representing a monetary amount"""

    amount: condecimal(gt=0, decimal_places=2) = Field(..., description="The amount of money")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency ISO code")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot subtract money with different currencies")
        return Money(amount=self.amount - other.amount, currency=self.currency)


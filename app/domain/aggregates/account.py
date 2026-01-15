from uuid import uuid4

from app.domain.aggregates.transaction import Transaction
from app.domain.events.balance_updated import BalanceUpdated
from app.domain.value_objects.money import Money


class Account:
    """Aggregate root for account"""

    def __init__(self, owner: str, balance: Money = None, pk: str = None):
        self.pk = pk or str(uuid4())
        self.owner = owner
        self.balance = balance or Money(0)
        self._transactions: list(Transaction) = []
        self.events: list = []

    @property
    def transactions(self) -> list(Transaction):
        """Get a copy of the transactions"""
        return self._transactions.copy()

    def deposit(self, amount: Money):
        """Deposit money into the account.

        Args:
            amount (Money): The amount to deposit.
        """
        if amount <= Money(0):
            raise ValueError("Amount must be greater than 0")
        self.balance += amount
        self._transactions.append(
            Transaction(
                from_account=None,
                to_account=self.pk,
                amount=amount,
                status="completed"
            )
        )

        self.events.append(BalanceUpdated(account_pk=self.pk, new_balance=self.balance))

    def withdraw(self, amount: Money):
        """Withdraw money from the account.

        Args:
            amount (Money): The amount to withdraw.
        """
        if self.balance.amount < amount.amount:
            raise ValueError("Insufficient funds")

        self.balance -= amount
        self._transactions.append(
            Transaction(
                from_account=self.pk,
                to_account=None,
                amount=amount,
                status="completed"
            )
        )

        self.events.append(BalanceUpdated(account_pk=self.pk, new_balance=self.balance))

    def transfer_to(self, target: "Account", amount: Money):
        """Transfer money to another account.

        Args:
            target (Account): The target account.
            amount (Money): The amount to transfer.
        """
        if amount.amount > self.balance.amount:
            raise ValueError("Insufficient funds")

        self.balance -= amount
        target.balance += amount
        self._transactions.append(
            Transaction(
                from_account=self.pk,
                to_account=target.pk,
                amount=amount,
                status="completed"
            )
        )

        self.events.append(BalanceUpdated(account_pk=self.pk, new_balance=self.balance))
        target.events.append(BalanceUpdated(account_pk=target.pk, new_balance=target.balance))
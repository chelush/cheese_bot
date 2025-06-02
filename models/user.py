from typing import Optional, Dict, Any
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime

from sqlmodel import SQLModel, Field, Column, JSON, DECIMAL, DateTime


def round_two_decimals(value) -> Optional[Decimal]:
    if value is None:
        return None
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class User(SQLModel, table=True):
    __tablename__ = "users"

    telegram_id: int = Field(primary_key=True, index=True, description="Telegram user ID")

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False),
        description="Когда пользователь впервые появился"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False),
        description="Когда в последний раз обновляли"
    )

    lang: Optional[str] = Field(default=None, description="Language code of the user")

    telegram: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Сериализованный aiogram.types.User"
    )

    is_admin: bool = Field(default=False, description="Is user admin")

    @classmethod
    def round_decimal_fields(cls, user: "User") -> "User":
        user.balance = round_two_decimals(user.balance)
        user.referral_balance = round_two_decimals(user.referral_balance)
        user.referral_bonus = round_two_decimals(user.referral_bonus)
        user.earned_by_referrals = round_two_decimals(user.earned_by_referrals)
        user.amount_of_purchases = round_two_decimals(user.amount_of_purchases)
        if user.referral_percent is not None:
            user.referral_percent = round_two_decimals(user.referral_percent)
        return user

    def __repr__(self) -> str:
        return f"User(telegram_id={self.telegram_id})"

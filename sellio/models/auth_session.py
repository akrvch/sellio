from datetime import datetime
from datetime import timedelta

from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sellio.models import Base


class AuthSession(Base):
    __tablename__ = "auth_session"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    phone: Mapped[str] = mapped_column(String(length=20), index=True)
    otp_code: Mapped[str] = mapped_column(String(length=4))
    session_token: Mapped[str | None] = mapped_column(
        String(length=64), index=True, unique=True, nullable=True
    )
    user_id: Mapped[int | None] = mapped_column(index=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    verified: Mapped[bool] = mapped_column(default=False)

    @staticmethod
    def create_expiration(minutes: int = 5) -> datetime:
        return datetime.utcnow() + timedelta(minutes=minutes)

    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at

    def is_valid_code(self, code: str) -> bool:
        return (
            self.otp_code == code
            and not self.is_expired()
            and not self.verified
        )

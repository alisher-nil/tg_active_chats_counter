from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.constants import (
    TG_FIRST_NAME_MAX_LENGTH,
    TG_LAST_NAME_MAX_LENGTH,
    TG_USERNAME_MAX_LENGTH,
)
from app.core.db import Base


class Users(Base):
    telegram_id: Mapped[int] = mapped_column(BigInteger())
    first_name: Mapped[Optional[str]] = mapped_column(
        String(TG_FIRST_NAME_MAX_LENGTH)
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(TG_LAST_NAME_MAX_LENGTH)
    )
    username: Mapped[Optional[str]] = mapped_column(
        String(TG_USERNAME_MAX_LENGTH)
    )
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

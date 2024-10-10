from typing import Optional

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from constants import (
    TG_FIRST_NAME_MAX_LENGTH,
    TG_LAST_NAME_MAX_LENGTH,
    TG_USERNAME_MAX_LENGTH,
)
from db import Base


class User(Base):
    id: Mapped[int] = mapped_column(BigInteger())
    first_name: Mapped[Optional[str]] = mapped_column(
        String(TG_FIRST_NAME_MAX_LENGTH)
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(TG_LAST_NAME_MAX_LENGTH)
    )
    username: Mapped[Optional[str]] = mapped_column(
        String(TG_USERNAME_MAX_LENGTH)
    )
    # created_at: Mapped(date)

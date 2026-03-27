from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(70), index=True)
    last_name: Mapped[str] = mapped_column(String(70), index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(120), unique=True)
    birthday: Mapped[str] = mapped_column(String(120))

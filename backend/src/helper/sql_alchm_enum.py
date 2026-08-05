from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum


def _enum_column(enum_cls: type[Enum], length: int = 50) -> SQLAlchemyEnum:
    """
    SQLite does not have native enums, so we use SQLAlchemy Enum with
    native_enum=False.

    values_callable makes the DB store the enum .value, for example:
        "male"
    instead of the enum .name, for example:
        "MALE"
    """
    return SQLAlchemyEnum(
        enum_cls,
        native_enum=False,
        length=length,
        values_callable=lambda obj: [member.value for member in obj],
    )

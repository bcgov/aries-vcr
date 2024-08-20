from enum import Enum


class MappingTypeEnum(str, Enum):
    """MappingType enum"""

    EFFECTIVE_DATE = "effective_date"
    REVOKED_DATE = "revoked_date"

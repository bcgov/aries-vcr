from enum import Enum


class MappingTypeEnum(str, Enum):
    """MappingType enum"""

    EFFECTIVE_DATE = "effective_date"
    EXPIRY_DATE = "expiry_date"
    REVOKED_DATE = "revoked_date"

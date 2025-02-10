from enum import Enum


class EmployeeStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class PaymentMethod(str, Enum):
    CASH = "cash"
    TRANSFER = "transfer"


class Currency(str, Enum):
    SOLES = "soles"
    DOLLARS = "dollars"


class AccountType(str, Enum):
    CURRENT = "current"
    SAVINGS = "savings"


class TransportType(str, Enum):
    VAN = "van"
    TRAILER = "trailer"


class UserRole(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
    MANAGER = "manager"
    AUDITOR = "auditor"

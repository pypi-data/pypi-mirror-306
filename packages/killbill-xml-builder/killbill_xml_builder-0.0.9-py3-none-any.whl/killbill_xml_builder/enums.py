import enum


class ProductCategory(enum.Enum):
    """Product category"""

    BASE = "BASE"
    ADD_ON = "ADD_ON"
    STANDALONE = "STANDALONE"

    def __str__(self):
        return self.value


class BillingMode(enum.Enum):
    """Billing Mode"""

    IN_ADVANCE = "IN_ADVANCE"
    IN_ARREAR = "IN_ARREAR"

    def __str__(self):
        return self.value


class TimeUnit(enum.Enum):
    """Time Unit"""

    DAYS = "DAYS"
    WEEKS = "WEEKS"
    MONTHS = "MONTHS"
    YEARS = "YEARS"
    UNLIMITED = "UNLIMITED"

    def __str__(self):
        return self.value


class BillingPeriod(enum.Enum):
    """Billing Period"""

    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    BIWEEKLY = "BIWEEKLY"
    THIRTY_DAYS = "THIRTY_DAYS"
    THIRTY_ONE_DAYS = "THIRTY_ONE_DAYS"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    BIANNUAL = "BIANNUAL"
    ANNUAL = "ANNUAL"
    SESQUIENNIAL = "SESQUIENNIAL"
    BIENNIAL = "BIENNIAL"
    TRIENNIAL = "TRIENNIAL"
    NO_BILLING_PERIOD = "NO_BILLING_PERIOD"

    def __str__(self):
        return self.value


class PhaseType(enum.Enum):
    """Plan Phases"""

    TRIAL = "TRIAL"
    DISCOUNT = "DISCOUNT"
    FIXEDTERM = "FIXEDTERM"
    EVERGREEN = "EVERGREEN"

    def __str__(self):
        return self.value


class BillingPolicy(enum.Enum):
    """Billing Policy"""

    START_OF_TERM = "START_OF_TERM"
    END_OF_TERM = "END_OF_TERM"
    IMMEDIATE = "IMMEDIATE"
    ILLEGAL = "ILLEGAL"

    def __str__(self):
        return self.value


class EntitlementPolicy(enum.Enum):
    """Entitlement Policy"""

    IMMEDIATE = "IMMEDIATE"
    END_OF_TERM = "END_OF_TERM"

    def __str__(self):
        return self.value


class BillingAlignmentPolicy(enum.Enum):
    """Billing Alignment Policy"""

    ACCOUNT = "ACCOUNT"
    SUBSCRIPTION = "SUBSCRIPTION"
    BUNDLE = "BUNDLE"

    def __str__(self):
        return self.value


class CreateAlignmentPolicy(enum.Enum):
    """Create Alignment Policy"""

    START_OF_BUNDLE = "START_OF_BUNDLE"
    START_OF_SUBSCRIPTION = "START_OF_SUBSCRIPTION"

    def __str__(self):
        return self.value


class ChangeAlignmentPolicy(enum.Enum):
    """Change Alignment Policy"""

    START_OF_BUNDLE = "START_OF_BUNDLE"
    START_OF_SUBSCRIPTION = "START_OF_SUBSCRIPTION"
    CHANGE_OF_PLAN = "CHANGE_OF_PLAN"
    CHANGE_OF_PRICELIST = "CHANGE_OF_PRICELIST"

    def __str__(self):
        return self.value

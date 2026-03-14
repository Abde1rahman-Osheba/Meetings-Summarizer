from enum import Enum


class ComplianceStatus(str, Enum):
    PASSED = "passed"
    WARNING = "warning"
    FAILED = "failed"

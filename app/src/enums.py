from enum import Enum


class ApplicationStatus(Enum):
    ALL = 0
    APPROVE = 1
    REJECT = 2
    PROCESSING = 3
    SUCCESSFUL = 4
    UNSUCCESSFUL = 5


class ClassesStatus(Enum):
    ALL = 0
    FUTURE = 1
    PAST = 2
    STARTED = 3
    ENROLMENT = 4

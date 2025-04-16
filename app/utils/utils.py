import enum

class Status(enum.Enum):
    #TODO: we can also add more statuses
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class Role(enum.Enum):
    LEAD = "LEAD"
    DEVELOPER = "DEVELOPER"
    TESTER = "TESTER"
    # DOCUMENTATOR = "DOCUMENTATOR"
    MANAGER = "MANAGER"
    DELIVERY = "DELIVERY"

class Complexity(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
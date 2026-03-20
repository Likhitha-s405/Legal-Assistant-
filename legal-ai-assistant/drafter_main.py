
from drafter.drafter import Drafter


def draft_api(data: dict):
    drafter = Drafter()
    result = drafter.draft(data)
    return result


class ApplicationStateMachine:
    """
    Minimal persisted state machine logic.
    transition(old -> new) returns (True, '') on success
    or (False, 'reason') on failure.
    """
    TRANSITIONS = {
        "applied": ["screening", "rejected"],
        "screening": ["interview", "rejected"],
        "interview": ["offer", "rejected"],
        "offer": ["hired", "rejected"],
        "hired": [],
        "rejected": []
    }

    def __init__(self, current_state: str):
        if current_state not in self.TRANSITIONS:
            # treat unknown as applied
            current_state = "applied"
        self.current = current_state

    def transition(self, to_state: str):
        # allow rejected from anywhere
        if to_state == "rejected":
            return True, ""
        allowed = self.TRANSITIONS.get(self.current, [])
        if to_state in allowed:
            return True, ""
        return False, f"Invalid transition from {self.current} to {to_state}"

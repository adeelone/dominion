from __future__ import annotations


BLOCKED_PATTERNS = ("sexual minor", "exterminate real group", "dox living person")


class ModerationPolicy:
    def check(self, text: str) -> tuple[bool, str]:
        lowered = text.lower()
        for pattern in BLOCKED_PATTERNS:
            if pattern in lowered:
                return False, f"Blocked by safety policy: {pattern}."
        return True, "Allowed."

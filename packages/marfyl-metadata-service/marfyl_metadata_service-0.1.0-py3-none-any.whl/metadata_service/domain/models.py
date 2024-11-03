from typing import List, Optional

class MetaData:
    def __init__(self, user_id: Optional[str], email: Optional[str], first_name: Optional[str],
                 last_name: Optional[str], subscription_id: Optional[str], language: str,
                 action_ids: List[int], permission_ids: List[int]):
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.subscription_id = subscription_id
        self.language = language
        self.action_ids = action_ids
        self.permission_ids = permission_ids

    @property
    def full_name(self) -> Optional[str]:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return None
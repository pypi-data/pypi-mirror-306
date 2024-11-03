from typing import Dict, List
from .models import MetaData

class MetaDataService:
    def __init__(self):
        self.meta_data = MetaData(None, None, None, None, None, "DEFAULT", [], [])

    def set_meta_data(self, header_values: Dict[str, str]) -> None:
        self.meta_data.user_id = header_values.get("UserId")
        self.meta_data.email = header_values.get("Email")
        self.meta_data.first_name = header_values.get("FirstName")
        self.meta_data.last_name = header_values.get("LastName")
        self.meta_data.subscription_id = header_values.get("SubscriptionId")
        self.meta_data.language = header_values.get("Accept-Language", "DEFAULT")
        self.meta_data.action_ids = list(map(int, header_values.get("ActionIds", "").split(","))) if header_values.get("ActionIds") else []
        self.meta_data.permission_ids = list(map(int, header_values.get("PermissionIds", "").split(","))) if header_values.get("PermissionIds") else []

    def has_permission(self, permission_id: int) -> bool:
        return permission_id in self.meta_data.permission_ids
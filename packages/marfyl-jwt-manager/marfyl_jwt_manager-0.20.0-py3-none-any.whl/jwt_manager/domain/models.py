class UserData:
    def __init__(self, payload: dict):
        self.user_id = payload.get("user_id")
        self.email = payload.get("email")
        self.first_name = payload.get("first_name")
        self.last_name = payload.get("last_name")
        self.subscription_id = payload.get("subscription_id")
        self.language = payload.get("language")
        self.action_ids = payload.get("action_ids")
        self.permission_ids = payload.get("permission_ids")
        for key, value in payload.items():
            setattr(self, key, value)

    def __repr__(self):
        return (f"<UserData(user_id={self.user_id}, "
                f"email={self.email}, "
                f"first_name={self.first_name}, "
                f"last_name={self.last_name}, "
                f"subscription_id={self.subscription_id}, "
                f"language={self.language}, "
                f"action_ids={self.action_ids}, "
                f"permission_ids={self.permission_ids})>"
                )
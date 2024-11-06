class UserData:
    def __init__(self, payload: dict):
        self.email = None
        self.user_id = None
        self.first_name = None
        self.last_name = None
        self.subscription_id = None
        self.language = None
        self.action_ids = None
        self.permission_ids = None
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
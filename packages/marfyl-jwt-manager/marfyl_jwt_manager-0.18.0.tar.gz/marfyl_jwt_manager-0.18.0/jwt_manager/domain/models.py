class UserData:
    def __init__(self, payload: dict):
        self.UserId = payload.get("UserId")
        self.Email = payload.get("Email")
        self.FirstName = payload.get("FirstName")
        self.LastName = payload.get("LastName")
        self.SubscriptionId = payload.get("SubscriptionId")
        self.Language = payload.get("Language")
        self.ActionIds = payload.get("ActionIds")
        self.PermissionIds = payload.get("PermissionIds")
        for key, value in payload.items():
            setattr(self, key, value)

    def __repr__(self):
        return (f"<UserData(UserId={self.UserId}, "
                f"Email={self.Email}, "
                f"FirstName={self.FirstName}, "
                f"LastName={self.LastName}, "
                f"SubscriptionId={self.SubscriptionId}, "
                f"Language={self.Language}, "
                f"ActionIds={self.ActionIds}, "
                f"PermissionIds={self.PermissionIds})>"
                )
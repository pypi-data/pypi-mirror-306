# Need to create
class ResourceManager:
    def __init__(self):
        self.resources = {}
        self.limits = {}

    def register_resource(self, name: str, limit: int):
        self.resources[name] = 0
        self.limits[name] = limit

    def allocate(self, name: str, amount: int) -> bool:
        if self.resources[name] + amount <= self.limits[name]:
            self.resources[name] += amount
            return True
        return False

    def release(self, name: str, amount: int):
        self.resources[name] = max(0, self.resources[name] - amount) 
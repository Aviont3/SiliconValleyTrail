# Game state in Silicon Valley Trail.

class GameState:
    """Represents the current state of the game."""

    MAX_DAYS = 60
    REVENUE_INTERVAL = 5

    def __init__(self):
        self.day = 0
        self.money = 3500
        self.chemistry = 25
        self.followers = 0
        self.location_index = 0
        self.won = False
        self.alive = True
        self.features = []
        self.features_meter = 0
        self.base_revenue = 100
        self.turns_since_revenue = 0
        self.product_progress = 5
        self.morale = 100
        self.team_members = []

    @property
    def features_multiplier(self):
        return len(self.features)

    def get_day(self):
        """Return the current day."""
        return self.day

    def days_left(self):
        """Calculate and return the number of days left in the game."""
        return max(0, self.MAX_DAYS - self.day)

    def advance_day(self, amount=1):
        """Advance the game by a number of days."""
        if amount <= 0:
            return
        self.day += amount

    def calculate_revenue(self):
        """Calculate and return the current revenue based on features and followers."""
        if self.turns_since_revenue < self.REVENUE_INTERVAL:
            return 0
        revenue = self.base_revenue * (1 + 0.5 * self.features_multiplier) * (1 + 0.01 * self.followers)
        self.turns_since_revenue = 0
        return int(revenue)
    
    def apply_effects(self, effects):
        """Apply a dictionary of effects to the game state."""
        for key, value in effects.items():
            if hasattr(self, key):
                setattr(self, key, getattr(self, key) + value)

    def get_location_name(self):
        """Return the name of the current location."""
        from data.locations import LOCATIONS
        if 0 <= self.location_index < len(LOCATIONS):
            return LOCATIONS[self.location_index]
        return "Unknown Location"
    def to_dict(self):
        """Convert the game state to a dictionary for easy serialization."""
        return {
            "day": self.day,
            "money": self.money,
            "chemistry": self.chemistry,
            "followers": self.followers,
            "location_index": self.location_index,
            "location": self.get_location_name(),
            "won": self.won,
            "alive": self.alive,
            "features": self.features,
            "features_multiplier": self.features_multiplier,
            "features_meter": self.features_meter,
            "product_progress": self.product_progress,
            "morale": self.morale,
            "team_members": self.team_members,
            "days_left": self.days_left(),
        }
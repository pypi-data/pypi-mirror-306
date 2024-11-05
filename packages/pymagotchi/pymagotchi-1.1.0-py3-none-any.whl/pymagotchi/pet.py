from time import time
from .names import generate_name
from .constants import DEFAULT_TIMEFRAME, MAX_STAT_VALUE

class Pet:
    def __init__(self, name=None, timeframe=DEFAULT_TIMEFRAME, immortal: bool = False):

        self.name = name if isinstance(name, str) else generate_name()
        self.immortal = immortal if isinstance(immortal, bool) else False
        self.timeframe = timeframe if isinstance(
            timeframe, (int, float)) and timeframe >= 1 else DEFAULT_TIMEFRAME

        self.current_time = int(time())

        self.stats = {
            "health": MAX_STAT_VALUE,
            "food": MAX_STAT_VALUE,
            "sleep": MAX_STAT_VALUE,
            "happiness": MAX_STAT_VALUE
        }
        self.rates = {
            "food": (self.timeframe * 60) // MAX_STAT_VALUE,
            "sleep": (self.timeframe * 60) // MAX_STAT_VALUE,
            "happiness": (self.timeframe * 60) // MAX_STAT_VALUE
        }

    # Returns the time since this function was last called
    def time_elapsed(self):
        new_time = int(time())
        difference = new_time - self.current_time
        self.current_time = new_time
        return difference

    # Decrement pet's stats based on the time passed
    def update_stats(self):
        difference = self.time_elapsed()
        for stat in ["food", "sleep", "happiness"]:
            if self.rates[stat] != 0:
                self.stats[stat] = max(0, self.stats[stat] - difference // self.rates[stat])
            else:
                self.stats[stat] = max(0, self.stats[stat])

        if not self.immortal:  
            self.stats["health"] = (self.stats["sleep"] + self.stats["food"] + self.stats["happiness"]) // 3
        else:
            self.stats["health"] = max(1, self.stats["health"])  # min of 1 health if immortal
        # self.stats["health"] = (
        #     self.stats["sleep"] + self.stats["food"] + self.stats["happiness"]) // 3

    # Print the pet's current stats
    def status(self):
        self.update_stats()
        parts = []
        for stat, value in self.stats.items():
            parts.append(f"{stat.capitalize()}: {value}")
        result = " | ".join(parts)
        print(result)

    def feed(self, amount):
        if not isinstance(amount, int) or amount < 0:
            print("Invalid food amount.")
            return
        self.stats["food"] = min(self.stats["food"] + amount, MAX_STAT_VALUE)
        print(f"{self.name} has been fed with {amount} food points!")

    def play(self, duration):
        if not isinstance(duration, int) or duration < 0:
            print("Invalid play duration.")
            return
        self.stats["happiness"] = min(self.stats["happiness"] + duration, MAX_STAT_VALUE)
        print(f"{self.name} enjoyed playing with you for {duration} time units!")

    def sleep(self, duration):
        if not isinstance(duration, int) or duration < 0:
            print("Invalid sleep duration.")
            return
        self.stats["sleep"] = min(self.stats["sleep"] + duration, MAX_STAT_VALUE)
        print(f"{self.name} slept for {duration} time units!")

    def rename(self, new_name):
        if isinstance(new_name, str) and new_name.strip():
            self.name = new_name
            print(f"Your pet's name is now {self.name}!")
        else:
            print("Invalid name. Please enter a valid name.")

    def display_art(self):
        """
        Shows ASCII art --> different expressions based on health, happiness, food, and sleep levels.
        """
        def get_primary_state():
            stats = {
                "health": self.stats["health"],
                "food": self.stats["food"],
                "sleep": self.stats["sleep"],
                "happiness": self.stats["happiness"]
            }
            lowest_stat = min(stats, key=stats.get)
            lowest_value = stats[lowest_stat]
            if lowest_value >= 80:
                return "excellent"
            elif lowest_value >= 60:
                return "good"
            elif lowest_value >= 40:
                return "fair"
            elif lowest_value >= 20:
                return "poor"
            else:
                return "critical"

        def get_sleep_indicator():
            if self.stats["sleep"] < 30:
                return "(-_-) zzz..."
            return ""

        def get_food_indicator():
            if self.stats["food"] < 30:
                return "(っ˘ڡ˘ς)"
            return ""
        # asciis
        expressions = {
            "excellent": r"""
            ∩∩
            (^▽^)
            (つ🎀⊂)
            U U""",
            
            "good": r"""
            ∩∩
            (´▽`)
            (つ⊂)
            U U""",
            
            "fair": r"""
            ∩∩
            (•́ω•̀)
            (つ⊂)
            U U""",
            
            "poor": r"""
            ∩∩
            (；ω；)
            (つ⊂)
            U U""",
            
            "critical": r"""
            ∩∩
            (╥﹏╥)
            (つ⊂)
            U U"""
        }

        current_state = get_primary_state()
        art = expressions[current_state]

        indicators = []
        sleep_indicator = get_sleep_indicator()
        food_indicator = get_food_indicator()
        
        if sleep_indicator:
            indicators.append(sleep_indicator)
        if food_indicator:
            indicators.append(food_indicator)

        print(f"\n{'-' * 20}")
        print(f"   {self.name}")
        print(art)
        if indicators:
            print(" ".join(indicators))
        print(f"{'-' * 20}")
        
        messages = {
            "excellent": f"{self.name} is very happy!",
            "good": f"{self.name} is doing well!",
            "fair": f"{self.name} could use some attention...",
            "poor": f"{self.name} needs care soon!",
            "critical": f"{self.name} needs immediate attention!"
        }
        print(messages[current_state])

# Wrapper to make new pet object
def new_pet(name=None, timeframe=None, immortal=False):

    if not isinstance(name, str):
        name = generate_name()
        print(f"Created new pet with random name: {name}.")

    else:
        print(f"Created new pet: {name}.")

    if not timeframe or timeframe < 1 or not isinstance(timeframe, (int, float)):
        timeframe = DEFAULT_TIMEFRAME
        print(f"Timeframe: {timeframe} minutes (default).")

    elif not isinstance(timeframe, (int, float)):
        print(
            f"Invalid timeframe. Timeframe defaulted to {timeframe} minutes.")

    else:
        print(f"Timeframe: {timeframe} minutes.")

    if immortal:
        print("Immortality: On")

    pet = Pet(name, timeframe, immortal)
    return pet

"""
def main():
    pet = new_pet(timeframe=-1)
    while (pet.stats["health"] > 0):
        sleep(1)
        pet.status()

if __name__ == "__main__":
    main()
"""


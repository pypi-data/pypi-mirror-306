import time
import freezegun
from pymagotchi.pet import Pet, new_pet
from pymagotchi.constants import DEFAULT_TIMEFRAME, MAX_STAT_VALUE
from pymagotchi.names import generate_name, pet_names

# 1) test Pet.time_elapsed()
@freezegun.freeze_time("2024-10-28")
def test_time_elapsed():
    """
    Test that time_elapsed correctly calculates time differences.
    multiple intervals: 2 minutes (120 seconds), 30 seconds, 1 hour (3600 seconds)
    """
    pet = Pet(timeframe=DEFAULT_TIMEFRAME)
    with freezegun.freeze_time("2024-10-28 00:02:00"):
        time_passed = pet.time_elapsed()
        assert time_passed == 120, f"Expected 120 seconds, got {time_passed}"
    with freezegun.freeze_time("2024-10-28 00:02:30"):
        time_passed = pet.time_elapsed()
        assert time_passed == 30, f"Expected 30 seconds, got {time_passed}"
    with freezegun.freeze_time("2024-10-28 01:02:30"):
        time_passed = pet.time_elapsed()
        assert time_passed == 3600, f"Expected 3600 seconds, got {time_passed}"

# 2) Test names.generate_name()
def test_generate_name_string():
    """Test that generated name is a string type."""
    name = generate_name()
    assert isinstance(name, str), f"Expected String, instead got {name}"

def test_generate_name_empty():
    """Test that generated name is not empty."""
    name = generate_name()
    assert len(name) > 0, f"Expected positive length, instead got {name}"

def test_generate_name_list():
    """Test that generated name exists in the pet_names list."""
    name = generate_name()
    assert name in pet_names, f"Expected {name} to be in names.pet_names list"

# 3) Test Pet.__init__()
@freezegun.freeze_time("2024-10-28 0:00:00")
def test_default_init():
    """Test pet initialization with default values for all parameters."""
    pet = Pet()
    assert pet.name in pet_names, "Expected valid pet name."
    assert pet.immortal is False, f"Default immortal should be False, instead is {pet.immortal}"
    assert pet.timeframe == DEFAULT_TIMEFRAME, f"Expected timeframe to be {DEFAULT_TIMEFRAME}, instead is {pet.timeframe}"
    assert pet.current_time == int(time.time())
    for stat in ["health", "food", "sleep", "happiness"]:
        assert pet.stats[stat] == MAX_STAT_VALUE
    for rate in ["food", "sleep", "happiness"]:
        assert pet.rates[rate] == ((pet.timeframe * 60) // MAX_STAT_VALUE)

@freezegun.freeze_time("2024-10-28 0:00:00")
def test_invalid_init():
    """Test pet initialization with invalid parameter values."""
    pet = Pet(name=[1, 2], timeframe=-1, immortal="test")
    assert pet.name in pet_names, "Expected valid pet name."
    assert pet.immortal is False, f"Default immortal should be False, instead is {pet.immortal}"
    assert pet.timeframe == DEFAULT_TIMEFRAME, f"Expected default timeframe to be {DEFAULT_TIMEFRAME}, instead is {pet.timeframe}"
    assert pet.current_time == int(time.time())
    for stat in ["health", "food", "sleep", "happiness"]:
        assert pet.stats[stat] == MAX_STAT_VALUE
    for rate in ["food", "sleep", "happiness"]:
        assert pet.rates[rate] == ((pet.timeframe * 60) // MAX_STAT_VALUE)

@freezegun.freeze_time("2024-10-28 0:00:00")
def test_pet_initialization():
    """Test pet initialization with valid custom values for all parameters."""
    pet = Pet(name="Benny", timeframe=5, immortal=True)
    assert pet.name == "Benny"
    assert pet.immortal is True
    assert pet.timeframe == 5
    assert pet.current_time == int(time.time())
    for stat in ["health", "food", "sleep", "happiness"]:
        assert pet.stats[stat] == MAX_STAT_VALUE
    for rate in ["food", "sleep", "happiness"]:
        assert pet.rates[rate] == ((pet.timeframe * 60) // MAX_STAT_VALUE)

# 4) Test new_pet() function
@freezegun.freeze_time("2024-10-28 0:00:00")
def test_new_pet_default():
    """Test new_pet function with default parameters."""
    pet = Pet()
    assert pet.name in pet_names, "Expected valid pet name."
    assert pet.immortal is False, f"Default immortal should be False, instead is {pet.immortal}"
    assert pet.timeframe == DEFAULT_TIMEFRAME, f"Expected timeframe to be {DEFAULT_TIMEFRAME}, instead is {pet.timeframe}"
    assert pet.current_time == int(time.time())
    for stat in ["health", "food", "sleep", "happiness"]:
        assert pet.stats[stat] == MAX_STAT_VALUE
    for rate in ["food", "sleep", "happiness"]:
        assert pet.rates[rate] == ((pet.timeframe * 60) // MAX_STAT_VALUE)

def test_new_pet_invalid_name():
    """Test new_pet function with various invalid name parameters."""
    pet = Pet(name=-12)
    assert pet.name in pet_names, f"Expected valid pet name. name = {pet.name}"
    pet = Pet(name=[1, 2])
    assert pet.name in pet_names, f"Expected valid pet name. name = {pet.name}"
    pet = Pet(name=None)
    assert pet.name in pet_names, f"Expected valid pet name. name = {pet.name}"

def test_new_pet_invalid_timeframe():
    """Test new_pet function with invalid timeframe values."""
    pet = Pet(timeframe=-12)
    assert pet.timeframe == DEFAULT_TIMEFRAME, f"Expected default timeframe {DEFAULT_TIMEFRAME}, instead got {pet.timeframe}"
    pet = Pet(timeframe=0)
    assert pet.timeframe == DEFAULT_TIMEFRAME, f"Expected default timeframe {DEFAULT_TIMEFRAME}, instead got {pet.timeframe}"
    pet = Pet(timeframe="test")
    assert pet.timeframe == DEFAULT_TIMEFRAME, f"Expected default timeframe {DEFAULT_TIMEFRAME}, instead got {pet.timeframe}"

def test_new_pet_invalid_immortal():
    """Test new_pet function with invalid immortal parameter."""
    pet = Pet(immortal=-12)
    assert pet.timeframe == DEFAULT_TIMEFRAME, f"Expected immortal=False, instead got {pet.timeframe}"

@freezegun.freeze_time("2024-10-28 0:00:00")
def test_new_pet():
    """Test new_pet function with all valid custom parameters."""
    pet = new_pet(name="Shadow", timeframe=3, immortal=False)
    assert pet.name == "Shadow", f"Expected name=Shadow, instead name={pet.name}"
    assert pet.timeframe == 3, f"Expected timeframe=3, instead timeframe={pet.timeframe}"
    assert pet.current_time == int(time.time())
    assert pet.immortal is False, f"Expected immortal=False, instead immortal={pet.immortal}"
    for stat in ["health", "food", "sleep", "happiness"]:
        assert pet.stats[stat] == MAX_STAT_VALUE
    for rate in ["food", "sleep", "happiness"]:
        assert pet.rates[rate] == ((pet.timeframe * 60) // MAX_STAT_VALUE)

# 5) Test Pet.update_stats()
@freezegun.freeze_time("2024-10-28 0:00:00")
def test_update_stats():
    """Test that stats properly decrease over time."""
    pet = Pet(timeframe=2)
    pet.stats["food"] = 50
    pet.stats["sleep"] = 50
    pet.stats["happiness"] = 50
    pet.stats["health"] = 50
    with freezegun.freeze_time("2024-10-28 0:10:00"):
        pet.update_stats()

    for stat in ["health", "food", "sleep", "happiness"]:
        assert pet.stats[stat] == 0, f"{stat} should have decremented with time"

@freezegun.freeze_time("2024-10-28 0:00:00")
def test_update_stats_zero():
    """Test that stats cannot go below zero."""
    pet = Pet(timeframe=1)
    pet.stats["food"] = 0
    pet.stats["sleep"] = 0
    pet.stats["happiness"] = 0
    with freezegun.freeze_time("2024-10-28 0:10:00"):
        pet.update_stats()

    for stat in ["health", "food", "sleep", "happiness"]:
        assert pet.stats[stat] == 0, f"{stat} should not be below 0"

@freezegun.freeze_time("2024-10-28 0:00:00")
def test_update_stats_rate():
    """Test that stats decrease at the correct rate based on timeframe."""
    pet = Pet(timeframe=10)
    with freezegun.freeze_time("2024-10-28 0:09:00"):
        pet.update_stats()

    for stat in ["health", "food", "sleep", "happiness"]:
        assert pet.stats[stat] == 10, f"{stat} should have decremented to 10, not {pet.stats[stat]}"

# 6) Test Pet.status() output
@freezegun.freeze_time("2024-10-28 0:00:00")
def test_pet_status_initial(capsys):
    """Test initial status output when pet is created."""
    pet = Pet()
    pet.status()
    captured = capsys.readouterr()
    assert "Health: 100 " in captured.out, "Expected 'Health: 100 ' in output"
    assert "Food: 100 " in captured.out, "Expected 'Food: 100 ' in output"
    assert "Sleep: 100 " in captured.out, "Expected 'Sleep: 100 ' in output"
    assert "Happiness: 100" in captured.out, "Expected 'Happiness: 100' in output"

@freezegun.freeze_time("2024-10-28 0:00:00")
def test_pet_status_zero(capsys):
    """Test status output when all stats are zero."""
    pet = Pet()
    with freezegun.freeze_time("2024-10-28 0:10:00"):
        pet.status()
    captured = capsys.readouterr()
    assert "Health: 0 " in captured.out, "Expected 'Health: 0 ' in output"
    assert "Food: 0 " in captured.out, "Expected 'Food: 0 ' in output"
    assert "Sleep: 0 " in captured.out, "Expected 'Sleep: 0 ' in output"
    assert "Happiness: 0" in captured.out, "Expected 'Happiness: 0' in output"

@freezegun.freeze_time("2024-10-28 0:00:00")
def test_pet_status_expected(capsys):
    """Test status output shows correct values after time passage."""
    pet = Pet(timeframe=DEFAULT_TIMEFRAME)

    with freezegun.freeze_time("2024-10-28 0:01:00"):
        pet.status()
    captured = capsys.readouterr()
    health = pet.stats["health"]
    food = pet.stats['food']
    sleep = pet.stats["sleep"]
    happiness = pet.stats["happiness"]
    assert f"Health: {health} " in captured.out, f"Expected 'Health: {health} ' in output"
    assert f"Food: {food} " in captured.out, f"Expected 'Food: {food} ' in output"
    assert f"Sleep: {sleep} " in captured.out, f"Expected 'Sleep: {sleep} ' in output"
    assert f"Happiness: {happiness}" in captured.out, f"Expected 'Happiness: {happiness}' in output"

# tests for feed() method
def test_feed_normal():
    """Test that feeding pet increases food stat by correct amount within normal range."""
    pet = Pet(name="TestPet")
    initial_food = pet.stats['food']
    pet.feed(10)
    assert pet.stats['food'] == min(initial_food+10, MAX_STAT_VALUE)

def test_feed_negative():
    """Test that feeding negative amount does not change food stat."""
    pet = Pet(name="TestPet")
    initial_food = pet.stats["food"]
    pet.feed(-10)
    assert pet.stats["food"] == initial_food

def test_feed_overflow():
    """Test that feeding does not increase food stat beyond maximum value."""
    pet = Pet(name="TestPet")
    pet.stats["food"] = 90
    pet.feed(20)
    assert pet.stats["food"] == MAX_STAT_VALUE

def test_feed_invalid_type(capsys):
    """Test that feeding invalid type does not change food stat and shows error."""
    pet = Pet(name="TestPet")
    initial_food = pet.stats["food"]
    pet.feed("not a number")
    captured = capsys.readouterr()
    assert "Invalid food amount" in captured.out
    assert pet.stats["food"] == initial_food

# tests for play() method
def test_play_normal():
    """Test that playing increases happiness stat by correct amount within normal range."""
    pet = Pet(name="TestPet")
    initial_happiness = pet.stats["happiness"]
    pet.play(10)
    assert pet.stats["happiness"] == min(initial_happiness + 10, MAX_STAT_VALUE)

def test_play_negative():
    """Test that negative play duration does not change happiness stat."""
    pet = Pet(name="TestPet")
    initial_happiness = pet.stats["happiness"]
    pet.play(-10)
    assert pet.stats["happiness"] == initial_happiness

def test_play_overflow():
    """Test that playing does not increase happiness stat beyond maximum value."""
    pet = Pet(name="TestPet")
    pet.stats["happiness"] = 90
    pet.play(20)
    assert pet.stats["happiness"] == MAX_STAT_VALUE

def test_play_invalid_type(capsys):
    """Test that invalid play duration does not change happiness stat and shows error."""
    pet = Pet(name="TestPet")
    initial_happiness = pet.stats["happiness"]
    pet.play("not a number")
    captured = capsys.readouterr()
    assert "Invalid play duration" in captured.out
    assert pet.stats["happiness"] == initial_happiness

#tests for sleep() method
def test_sleep_normal():
    """Test that sleeping increases sleep stat by correct amount within normal range."""
    pet = Pet(name="TestPet")
    initial_sleep = pet.stats["sleep"]
    pet.sleep(10)
    assert pet.stats["sleep"] == min(initial_sleep + 10, MAX_STAT_VALUE)

def test_sleep_negative():
    """Test that negative sleep duration does not change sleep stat."""
    pet = Pet(name="TestPet")
    initial_sleep = pet.stats["sleep"]
    pet.sleep(-10)
    assert pet.stats["sleep"] == initial_sleep

def test_sleep_overflow():
    """Test that sleeping does not increase sleep stat beyond maximum value."""
    pet = Pet(name="TestPet")
    pet.stats["sleep"] = 90
    pet.sleep(20)
    assert pet.stats["sleep"] == MAX_STAT_VALUE

def test_sleep_invalid_type(capsys):
    """Test that invalid sleep duration does not change sleep stat and shows error."""
    pet = Pet(name="TestPet")
    initial_sleep = pet.stats["sleep"]
    pet.sleep("not a number")
    captured = capsys.readouterr()
    assert "Invalid sleep duration" in captured.out
    assert pet.stats["sleep"] == initial_sleep

# tests for rename() method
def test_rename_normal():
    """Test that renaming pet changes name to new valid name."""
    pet = Pet(name="TestPet")
    pet.rename("NewName")
    assert pet.name == "NewName"

def test_rename_empty(capsys):
    """Test that empty name is rejected and original name is kept."""
    pet = Pet(name="TestPet")
    original_name = pet.name
    pet.rename("")
    captured = capsys.readouterr()
    assert "Invalid name" in captured.out
    assert pet.name == original_name

def test_rename_invalid_type(capsys):
    """Test that non-string name is rejected and original name is kept."""
    pet = Pet(name="TestPet")
    original_name = pet.name
    pet.rename(123)
    captured = capsys.readouterr()
    assert "Invalid name" in captured.out
    assert pet.name == original_name

#tests for display_art() method
def test_display_art_healthy(capsys):
    """Test that healthy pet displays appropriate happy face art."""
    pet = Pet(name="TestPet")
    pet.stats["health"] = 100
    pet.display_art()
    captured = capsys.readouterr()
    assert "(^▽^)" in captured.out

def test_display_art_unhealthy(capsys):
    """Test that unhealthy pet displays appropriate sad face art."""
    pet = Pet(name="TestPet")
    pet.stats["health"] = 20
    pet.display_art()
    captured = capsys.readouterr()
    assert "(；ω；)" in captured.out

def test_display_art_border_cases(capsys):
    """Test that medium health displays appropriate neutral face art."""
    pet = Pet(name="TestPet")
    pet.stats["health"] = 50
    pet.display_art()
    captured = capsys.readouterr()
    assert any(face in captured.out for face in ["(•́ω•̀)", "(；ω；)"])

# additional tests for health calculation
@freezegun.freeze_time("2024-10-28 0:00:00")
def test_health_calculation():
    """Test that health is correctly calculated as average of other stats."""
    pet = Pet(timeframe=1)
    pet.stats["food"] = 60
    pet.stats["sleep"] = 60
    pet.stats["happiness"]=60
    pet.update_stats()
    assert pet.stats["health"] == 60

@freezegun.freeze_time("2024-10-28 0:00:00")
def test_health_max():
    """Test that health calculation correctly handles maximum stat values."""
    pet = Pet(timeframe=1)
    pet.stats["food"] = MAX_STAT_VALUE
    pet.stats["sleep"] = MAX_STAT_VALUE
    pet.stats["happiness"] = MAX_STAT_VALUE
    pet.update_stats()
    assert pet.stats["health"] == MAX_STAT_VALUE

@freezegun.freeze_time("2024-10-28 0:00:00")
def test_health_min():
    """Test that health calculation correctly handles minimum stat values."""
    pet = Pet(timeframe=1)
    pet.stats["food"] = 0
    pet.stats["sleep"] = 0
    pet.stats["happiness"]= 0
    pet.update_stats()
    assert pet.stats["health"]== 0

# test immortality feature
@freezegun.freeze_time("2024-10-28 0:00:00")
def test_immortal_pet():
    """Test that immortal pet maintains health above zero."""
    pet = Pet(name="TestPet", immortal=True)
    with freezegun.freeze_time("2024-10-28 1:00:00"):
        pet.update_stats()
        assert pet.stats["health"] > 0

def test_immortal_vs_mortal():
    """Test that immortal pet survives while mortal pet's health drops to zero."""
    with freezegun.freeze_time("2024-10-28 0:00:00"):   #immortal vs mortal pets over time
        immortal_pet = Pet(name="ImmortalPet", immortal=True)
        mortal_pet = Pet(name="MortalPet", immortal=False)
        with freezegun.freeze_time("2024-10-28 12:00:00"):
            immortal_pet.update_stats()
            mortal_pet.update_stats()
            assert immortal_pet.stats["health"] >0
            assert mortal_pet.stats["health"] == 0

def test_immortal_pet_stat_changes():
    """Test that immortal pet's stats change normally while health stays above zero."""
    with freezegun.freeze_time("2024-10-28 0:00:00"):
        pet = Pet(name="TestPet", immortal=True)
        initial_stats = pet.stats.copy()
        with freezegun.freeze_time("2024-10-28 0:30:00"):
            pet.update_stats()
            assert pet.stats["food"] < initial_stats["food"]
            assert pet.stats["sleep"] < initial_stats["sleep"]
            assert pet.stats["happiness"] < initial_stats["happiness"]
            assert pet.stats["health"] > 0

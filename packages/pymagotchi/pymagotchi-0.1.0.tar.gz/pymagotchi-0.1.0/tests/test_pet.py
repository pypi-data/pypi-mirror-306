import time
import pytest
import freezegun
from pymagotchi.pet import Pet, new_pet
from pymagotchi.constants import DEFAULT_TIMEFRAME, MAX_STAT_VALUE
from pymagotchi.names import generate_name, pet_names


# 1) Test Pet.time_elapsed()
@freezegun.freeze_time("2024-10-28")
def test_time_elapsed():
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
    name = generate_name()
    assert isinstance(name, str), f"Expected String, instead got {name}"


def test_generate_name_empty():
    name = generate_name()
    assert len(name) > 0, f"Expected positive length, instead got {name}"


def test_generate_name_list():
    name = generate_name()
    assert name in pet_names, f"Expected {name} to be in names.pet_names list"


# 3) Test Pet.__init__()
@freezegun.freeze_time("2024-10-28 0:00:00")
def test_default_init():
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
    pet = Pet(name=-12)
    assert pet.name in pet_names, f"Expected valid pet name. name = {pet.name}"
    pet = Pet(name=[1, 2])
    assert pet.name in pet_names, f"Expected valid pet name. name = {pet.name}"
    pet = Pet(name=None)
    assert pet.name in pet_names, f"Expected valid pet name. name = {pet.name}"


def test_new_pet_invalid_timeframe():
    pet = Pet(timeframe=-12)
    assert pet.timeframe == DEFAULT_TIMEFRAME, f"Expected default timeframe {DEFAULT_TIMEFRAME}, instead got {pet.timeframe}"

    pet = Pet(timeframe=0)
    assert pet.timeframe == DEFAULT_TIMEFRAME, f"Expected default timeframe {DEFAULT_TIMEFRAME}, instead got {pet.timeframe}"

    pet = Pet(timeframe="test")
    assert pet.timeframe == DEFAULT_TIMEFRAME, f"Expected default timeframe {DEFAULT_TIMEFRAME}, instead got {pet.timeframe}"


def test_new_pet_invalid_immortal():
    pet = Pet(immortal=-12)
    assert pet.timeframe == DEFAULT_TIMEFRAME, f"Expected immortal=False, instead got {pet.timeframe}"


@freezegun.freeze_time("2024-10-28 0:00:00")
def test_new_pet():
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
    pet = Pet(timeframe=10)
    with freezegun.freeze_time("2024-10-28 0:09:00"):
        pet.update_stats()

    for stat in ["health", "food", "sleep", "happiness"]:
        assert pet.stats[stat] == 10, f"{stat} should have decremented to 10, not {pet.stats[stat]}"


# 6) Test Pet.status() output
@freezegun.freeze_time("2024-10-28 0:00:00")
def test_pet_status_initial(capsys):
    pet = Pet()
    pet.status()

    captured = capsys.readouterr()
    assert "Health: 100 " in captured.out, "Expected 'Health: 100 ' in output"
    assert "Food: 100 " in captured.out, "Expected 'Food: 100 ' in output"
    assert "Sleep: 100 " in captured.out, "Expected 'Sleep: 100 ' in output"
    assert "Happiness: 100" in captured.out, "Expected 'Happiness: 100' in output"


@freezegun.freeze_time("2024-10-28 0:00:00")
def test_pet_status_zero(capsys):
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

import pytest
from recycling_rewards import reward_points, collection_accepted, slot_status


# ===================== reward_points — Branch Coverage Tests =====================
# Every if/else must evaluate to BOTH True and False.

# --- Branch: material not in MIN_KG (line 5) ---
def test_valid_material_paper():
    """Branch 5 -> False: material IS in MIN_KG"""
    assert reward_points("paper", 3, False) == 0

def test_invalid_material():
    """Branch 5 -> True: material NOT in MIN_KG"""
    with pytest.raises(ValueError, match="unknown material"):
        reward_points("glass", 5, False)


# --- Branch: weight_kg < 0 (line 7) ---
def test_positive_weight():
    """Branch 7 -> False: weight >= 0"""
    assert reward_points("paper", 3, False) == 0

def test_negative_weight():
    """Branch 7 -> True: weight < 0"""
    with pytest.raises(ValueError, match="invalid weight"):
        reward_points("paper", -1, False)


# --- Branch: has_bonus and material != "metal" (line 10) ---
def test_bonus_non_metal():
    """Branch 10 -> True: has_bonus=True, material=paper (not metal)"""
    # minimum = 5 - 1 = 4, weight = 10, extra = 6, rate = 6 -> 36
    assert reward_points("paper", 10, True) == 36

def test_bonus_metal():
    """Branch 10 -> False (partial): has_bonus=True but material=metal"""
    # minimum stays 2, weight = 10, extra = 8, rate = 12 -> 96
    assert reward_points("metal", 10, True) == 96

def test_no_bonus():
    """Branch 10 -> False: has_bonus=False"""
    assert reward_points("paper", 10, False) == 30


# --- Branch: extra <= 0 (line 13) ---
def test_extra_zero():
    """Branch 13 -> True: extra == 0 -> return 0"""
    assert reward_points("paper", 5, False) == 0

def test_extra_negative():
    """Branch 13 -> True: extra < 0 -> return 0"""
    assert reward_points("paper", 2, False) == 0

def test_extra_positive():
    """Branch 13 -> False: extra > 0"""
    assert reward_points("paper", 10, False) == 30


# --- Branch: material == "metal" (line 15) ---
def test_material_is_metal():
    """Branch 15 -> True: material == metal -> rate = 12"""
    assert reward_points("metal", 10, False) == 96

def test_material_is_not_metal():
    """Branch 15 -> False: material != metal -> rate = 6"""
    assert reward_points("paper", 10, False) == 30


# --- Branch: extra > 20 (line 19) ---
def test_extra_within_20():
    """Branch 19 -> False: extra <= 20"""
    # paper: minimum=5, weight=10, extra=5, rate=6 -> 30
    assert reward_points("paper", 10, False) == 30

def test_extra_above_20_non_metal():
    """Branch 19 -> True, line 20: extra > 20, non-metal -> rate = 6+4 = 10"""
    # paper: minimum=5, weight=30, extra=25, rate=10 -> 250
    assert reward_points("paper", 30, False) == 250

def test_extra_above_20_metal():
    """Branch 19 -> True AND Branch 21 -> True: extra > 20, metal -> rate = 12+4+2 = 18"""
    # metal: minimum=2, weight=25, extra=23, rate=18 -> 414
    assert reward_points("metal", 25, False) == 414


# --- Branch: material == "metal" inside extra > 20 block (line 21) ---
def test_extra_above_20_plastic():
    """Branch 21 -> False: extra > 20 but material is plastic (not metal)"""
    # plastic: minimum=3, weight=30, extra=27, rate=6+4=10 -> 270
    assert reward_points("plastic", 30, False) == 270


# ===================== collection_accepted — Branch Coverage Tests =====================

# --- Branch: is_hazardous (line 27) ---
def test_hazardous_true_within_limit():
    """Branch 27 -> True, weight <= 5 -> True"""
    assert collection_accepted(5, 1, True) is True

def test_hazardous_true_over_limit():
    """Branch 27 -> True, weight > 5 -> False"""
    assert collection_accepted(10, 1, True) is False

def test_hazardous_false():
    """Branch 27 -> False: not hazardous"""
    assert collection_accepted(20, 2, False) is True


# --- Branch: weight_kg > 50 (line 29) ---
def test_weight_over_50():
    """Branch 29 -> True: weight > 50 -> False"""
    assert collection_accepted(60, 2, False) is False

def test_weight_within_50():
    """Branch 29 -> False: weight <= 50"""
    assert collection_accepted(20, 2, False) is True


# --- Branch: bags <= 3 (line 31) ---
def test_bags_within_limit():
    """Branch 31 -> True: bags <= 3"""
    assert collection_accepted(20, 3, False) is True

def test_bags_over_limit():
    """Branch 31 -> False: bags > 3"""
    assert collection_accepted(20, 5, False) is False


# ===================== slot_status — Branch Coverage Tests =====================

# --- Branch: is_morning (line 35) ---
def test_morning_slot():
    """Branch 35 -> True: cutoff = 20"""
    assert slot_status(25, True, False) == "open"

def test_afternoon_slot():
    """Branch 35 -> False: cutoff = 10"""
    assert slot_status(15, False, False) == "open"


# --- Branch: is_holiday (line 39) ---
def test_holiday_slot():
    """Branch 39 -> True: cutoff += 15"""
    # morning + holiday: cutoff = 20 + 15 = 35
    assert slot_status(35, True, True) == "open"

def test_non_holiday_slot():
    """Branch 39 -> False: cutoff unchanged"""
    assert slot_status(25, True, False) == "open"


# --- Branch: minutes_left >= cutoff (line 41) ---
def test_minutes_at_cutoff():
    """Branch 41 -> True: minutes == cutoff -> open"""
    assert slot_status(20, True, False) == "open"

def test_minutes_above_cutoff():
    """Branch 41 -> True: minutes > cutoff -> open"""
    assert slot_status(30, True, False) == "open"

def test_minutes_below_cutoff():
    """Branch 41 -> False: minutes < cutoff"""
    assert slot_status(10, True, False) == "late"


# --- Branch: minutes_left >= cutoff - 15 (line 43) ---
def test_minutes_in_late_range():
    """Branch 43 -> True: cutoff - 15 <= minutes < cutoff -> late"""
    # morning cutoff=20, cutoff-15=5, minutes=10 -> late
    assert slot_status(10, True, False) == "late"

def test_minutes_at_late_boundary():
    """Branch 43 -> True: minutes == cutoff - 15 -> late"""
    # morning cutoff=20, cutoff-15=5
    assert slot_status(5, True, False) == "late"

def test_minutes_below_late_range():
    """Branch 43 -> False: minutes < cutoff - 15 -> missed"""
    # morning cutoff=20, cutoff-15=5, minutes=3 -> missed
    assert slot_status(3, True, False) == "missed"


# --- Afternoon missed test ---
def test_afternoon_missed():
    """Afternoon cutoff=10, cutoff-15=-5, minutes=-1 is not possible, so 0 -> late"""
    # cutoff=10, cutoff-15=-5, minutes=0 >= -5 -> late
    assert slot_status(0, False, False) == "late"

def test_morning_missed():
    """Morning cutoff=20, cutoff-15=5, minutes=2 < 5 -> missed"""
    assert slot_status(2, True, False) == "missed"


# --- Holiday afternoon late and missed ---
def test_afternoon_holiday_open():
    """Afternoon + holiday: cutoff = 10+15=25, minutes=25 -> open"""
    assert slot_status(25, False, True) == "open"

def test_afternoon_holiday_late():
    """Afternoon + holiday: cutoff=25, cutoff-15=10, minutes=15 -> late"""
    assert slot_status(15, False, True) == "late"

def test_afternoon_holiday_missed():
    """Afternoon + holiday: cutoff=25, cutoff-15=10, minutes=5 -> missed"""
    assert slot_status(5, False, True) == "missed"

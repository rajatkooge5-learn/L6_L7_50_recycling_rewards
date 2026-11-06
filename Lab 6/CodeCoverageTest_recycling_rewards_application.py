import pytest
from recycling_rewards import reward_points, collection_accepted, slot_status


# ===================== reward_points tests =====================

def test_unknown_material_raises():
    """Line 5-6: material not in MIN_KG -> raise ValueError"""
    with pytest.raises(ValueError, match="unknown material"):
        reward_points("glass", 5, False)


def test_negative_weight_raises():
    """Line 7-8: weight_kg < 0 -> raise ValueError"""
    with pytest.raises(ValueError, match="invalid weight"):
        reward_points("paper", -1, False)


def test_paper_below_minimum_no_bonus():
    """Line 9-14: paper, weight <= minimum (5), no bonus -> return 0"""
    assert reward_points("paper", 3, False) == 0


def test_paper_above_minimum_no_bonus():
    """Line 9, 12-14, 17-18, 23: paper, weight > minimum, extra <= 20 -> extra * 6"""
    # minimum = 5, weight = 10, extra = 5, rate = 6 -> 30
    assert reward_points("paper", 10, False) == 30


def test_paper_with_bonus():
    """Line 10-11: has_bonus and material != metal -> minimum -= 1"""
    # minimum = 5 - 1 = 4, weight = 10, extra = 6, rate = 6 -> 36
    assert reward_points("paper", 10, True) == 36


def test_metal_no_bonus_above_minimum():
    """Line 10, 15-16, 23: metal, no bonus, extra <= 20 -> extra * 12"""
    # minimum = 2, weight = 10, extra = 8, rate = 12 -> 96
    assert reward_points("metal", 10, False) == 96


def test_metal_with_bonus_minimum_unchanged():
    """Line 10: metal with bonus -> minimum stays 2 (bonus skipped for metal)"""
    # minimum = 2, weight = 10, extra = 8, rate = 12 -> 96
    assert reward_points("metal", 10, True) == 96


def test_paper_extra_above_20():
    """Line 19-20: extra > 20 for non-metal -> rate = 6 + 4 = 10"""
    # minimum = 5, weight = 30, extra = 25, rate = 6+4 = 10 -> 250
    assert reward_points("paper", 30, False) == 250


def test_metal_extra_above_20():
    """Line 19-22: extra > 20 for metal -> rate = 12 + 4 + 2 = 18"""
    # minimum = 2, weight = 25, extra = 23, rate = 12+4+2 = 18 -> 414
    assert reward_points("metal", 25, False) == 414


def test_plastic_above_minimum():
    """Test plastic material path"""
    # minimum = 3, weight = 5, extra = 2, rate = 6 -> 12
    assert reward_points("plastic", 5, False) == 12


def test_exactly_at_minimum():
    """extra == 0 -> return 0"""
    assert reward_points("paper", 5, False) == 0


# ===================== collection_accepted tests =====================

def test_hazardous_within_limit():
    """Line 27-28: is_hazardous True, weight <= 5 -> True"""
    assert collection_accepted(5, 1, True) is True


def test_hazardous_over_limit():
    """Line 27-28: is_hazardous True, weight > 5 -> False"""
    assert collection_accepted(10, 1, True) is False


def test_non_hazardous_weight_over_50():
    """Line 29-30: not hazardous, weight > 50 -> False"""
    assert collection_accepted(60, 2, False) is False


def test_non_hazardous_within_limits():
    """Line 31: not hazardous, weight <= 50, bags <= 3 -> True"""
    assert collection_accepted(20, 2, False) is True


def test_non_hazardous_too_many_bags():
    """Line 31: not hazardous, weight <= 50, bags > 3 -> False"""
    assert collection_accepted(20, 5, False) is False


# ===================== slot_status tests =====================

def test_morning_open():
    """Line 35-36, 41-42: morning, no holiday, minutes >= cutoff(20) -> open"""
    assert slot_status(25, True, False) == "open"


def test_afternoon_open():
    """Line 37-38, 41-42: not morning, no holiday, minutes >= cutoff(10) -> open"""
    assert slot_status(15, False, False) == "open"


def test_morning_late():
    """Line 35-36, 43-44: morning, minutes in [cutoff-15, cutoff) -> late"""
    assert slot_status(10, True, False) == "late"


def test_afternoon_late():
    """Line 37-38, 43-44: afternoon, minutes in [cutoff-15, cutoff) -> late"""
    assert slot_status(5, False, False) == "late"


def test_missed():
    """Line 45: minutes < cutoff - 15 -> missed"""
    assert slot_status(0, True, False) == "missed"


def test_holiday_increases_cutoff():
    """Line 39-40: holiday adds 15 to cutoff"""
    # morning cutoff = 20 + 15 = 35, minutes = 35 -> open
    assert slot_status(35, True, True) == "open"


def test_afternoon_holiday_late():
    """Line 37-38, 39-40, 43-44: afternoon holiday, cutoff = 10+15 = 25"""
    # minutes = 15, cutoff = 25, cutoff-15 = 10, 15 >= 10 -> late
    assert slot_status(15, False, True) == "late"

from hypothesis import given, strategies as st
from processor import parse_collection, weight_average, net_points

# ---- Test 1: Fuzz parse_collection ----
# Property: parse_collection should never crash on any string or None input.
# It should either return a valid (material, weight) tuple or handle errors gracefully.
@given(st.text() | st.none())
def test_parse_collection_no_crash(s):
    try:
        parse_collection(s)
    except Exception as e:
        assert False, f"parse_collection crashed with: {e}"

# ---- Test 2: Fuzz weight_average ----
# Property: weight_average should never crash on any string or None input.
# It should return an integer average or handle invalid inputs gracefully.
@given(st.text() | st.none())
def test_weight_average_no_crash(s):
    try:
        weight_average(s)
    except Exception as e:
        assert False, f"weight_average crashed with: {e}"

# ---- Test 3: Fuzz net_points ----
# Property: net_points should never crash on any string or None input.
# It should return a non-negative number or handle errors gracefully.
@given(st.text() | st.none())
def test_net_points_no_crash(s):
    try:
        net_points(s)
    except Exception as e:
        assert False, f"net_points crashed with: {e}"

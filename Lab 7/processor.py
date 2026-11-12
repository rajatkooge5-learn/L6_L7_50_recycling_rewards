import math

def parse_collection(text):
    """Parse 'material:weight' string into (material_name, weight_kg) tuple.
    Returns None for any invalid or unexpected input."""
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    material = parts[0].strip()
    kg_str = parts[1].strip()
    if not material or not kg_str:
        return None
    try:
        kg = float(kg_str)
    except ValueError:
        return None
    if math.isnan(kg) or math.isinf(kg) or kg < 0:
        return None
    return material.title(), kg

def weight_average(weights_csv):
    """Calculate integer average of comma-separated weights.
    Returns 0 for any invalid or unexpected input."""
    if not isinstance(weights_csv, str):
        return 0
    parts = [p.strip() for p in weights_csv.split(',') if p.strip()]
    if not parts:
        return 0
    values = []
    for p in parts:
        try:
            values.append(int(p))
        except ValueError:
            return 0
    if not values:
        return 0
    return sum(values) // len(values)

def net_points(text):
    """Calculate net reward points as (points * 2 - penalty), minimum 0.
    Returns 0.0 for any invalid or unexpected input."""
    if not isinstance(text, str):
        return 0.0
    parts = text.split('|')
    if len(parts) != 2:
        return 0.0
    points_str = parts[0].strip()
    penalty_str = parts[1].strip()
    if not points_str or not penalty_str:
        return 0.0
    try:
        points = float(points_str)
        penalty = float(penalty_str)
    except ValueError:
        return 0.0
    if math.isnan(points) or math.isinf(points):
        return 0.0
    if math.isnan(penalty) or math.isinf(penalty):
        return 0.0
    total = points * 2 - penalty
    return max(total, 0.0)

def main():
    print("==== Running parse_collection ====")
    user_input = input("Enter material:weight in kg (e.g. paper:12): ")
    result = parse_collection(user_input)
    print("Material and Weight:", result)

    print("\n==== Running weight_average ====")
    user_input = input("Enter weights in kg as CSV (e.g. 5,12,20): ")
    result = weight_average(user_input)
    print("Average Weight:", result)

    print("\n==== Running net_points ====")
    user_input = input("Enter points|penalty (e.g. 80|10): ")
    result = net_points(user_input)
    print("Net Points:", result)

if __name__ == "__main__":
    main()

import math

def parse_collection(text):
    if not isinstance(text, str):
        return None
    try:
        parts = text.split(':')
        if len(parts) != 2:
            return None
        material = parts[0].strip()
        if not material:
            return None
        kg_str = parts[1].strip()
        if not kg_str:
            return None
        kg = float(kg_str)
        if math.isnan(kg) or math.isinf(kg) or kg < 0:
            return None
        return material.title(), kg
    except (ValueError, TypeError):
        return None

def weight_average(weights_csv):
    if not isinstance(weights_csv, str):
        return 0
    try:
        parts = [r.strip() for r in weights_csv.split(',') if r.strip()]
        if not parts:
            return 0
        values = []
        for r in parts:
            values.append(int(r))
        if not values:
            return 0
        return sum(values) // len(values)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

def net_points(text):
    if not isinstance(text, str):
        return 0.0
    try:
        parts = text.split('|')
        if len(parts) != 2:
            return 0.0
        points_str, penalty_str = parts[0].strip(), parts[1].strip()
        if not points_str or not penalty_str:
            return 0.0
        points = float(points_str)
        penalty = float(penalty_str)
        if math.isnan(points) or math.isnan(penalty) or math.isinf(points) or math.isinf(penalty):
            return 0.0
        total = points * 2 - penalty
        return max(total, 0.0)
    except (ValueError, TypeError):
        return 0.0

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

import json
import pandas as pd

def clean_list(strings):
    """Cleans a list of strings by removing extra spaces, converting to uppercase, and filtering out items with '**'."""
    result = []
    for s in strings:
        cleaned =" ".join(str(s).split()).upper()
        if "*" not in cleaned and cleaned != "NAN":
            result.append(cleaned)
    return result

def extract_meals(file_path):
    """Reads an Excel file and organizes meal data by date, ensuring dates are correctly formatted without time components."""
    df = pd.read_excel(file_path)
    meal_data = {}
    week_days = "monday tuesday wednesday thursday friday saturday sunday"

    for col in df.columns:
        column_data = df[col].dropna()
        column_data = column_data.astype(str)
        column_data = column_data.str.strip()
        column_data = column_data.tolist()
        # Remove week day names
        column_data = [item.lower() for item in column_data if item.lower() not in week_days]

        # Convert first item to a proper date format
        date = pd.to_datetime(column_data[0]).date().isoformat()  # Ensures only YYYY-MM-DD

        meals = {"BREAKFAST": [], "LUNCH": [], "DINNER": []}
        current_meal = None

        for item in column_data[1:]:  # Skip the date
            item_upper = item.upper()
            if item_upper in meals:
                current_meal = item_upper
            elif current_meal:
                meals[current_meal].append(item)

        for meal in meals:
            meals[meal] = clean_list(meals[meal]) if any(meals[meal]) else []

        meal_data[date] = meals

    return meal_data


file_path = "Mess Menu Sample.xlsx"
parsed_data = extract_meals(file_path)

jf = open("mess_menu.json","w+")
json.dump(parsed_data, jf, indent=3)
jf.close()
import json
import os
from datetime import datetime


class FoodLog:
    def __init__(self, username, log=None):
        self.username = username
        self.log_path = f"{self.username}_food_log.json"

        if log is not None:
            # Use the provided log (useful for testing)
            self.log = log
        else:
            self.log = self.load_log()

    def load_log(self):
        if os.path.exists(self.log_path):
            with open(self.log_path, "r") as file:
                return json.load(file)
        else:
            return []

    def save_log(self):
        with open(self.log_path, "w") as file:
            json.dump(self.log, file)

    def log_food(self, user_profile):
        date_str = datetime.now().strftime("%Y-%m-%d")
        print("\nLogging Food Intake:")
        food_name = input("Enter food name: ").strip().lower()
        category = input("Enter food category: ").strip().lower()
        calories = int(input("Enter calories (kcal): "))

        # Validate input
        if not food_name or not category or calories <= 0:
            print("Invalid input. Please try again.")
            return

        entry = {
            "date": date_str,
            "food": food_name,
            "category": category,
            "calories": calories,
        }

        # Append to logs and save
        self.log.append(entry)
        self.save_log()
        print(f"Successfully logged {calories} kcal for {food_name}.")

    def get_daily_calories(self, date_str):
        return sum(entry["calories"] for entry in self.log if entry["date"] == date_str)

    def get_logs_in_date_range(self, start_date=None, end_date=None):
        # For simplicity, return all logs (expand as needed)
        return self.log

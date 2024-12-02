import json
import os


class User:
    def __init__(self, username, profile=None):
        self.username = username
        self.profile_path = f"{self.username}_profile.json"

        if profile is not None:
            # Use the provided profile (useful for testing)
            self.profile = profile
        else:
            self.profile = self.load_profile()

    def load_profile(self):
        if os.path.exists(self.profile_path):
            with open(self.profile_path, "r") as file:
                return json.load(file)
        else:
            return self.create_profile()

    def create_profile(self):
        print("Creating a new user profile.")
        weight = float(input("Enter your weight (kg): "))
        height = float(input("Enter your height (cm): "))
        age = int(input("Enter your age: "))
        daily_calorie_limit = int(input("Set your daily calorie limit (kcal): "))
        block_list = {"foods": [], "categories": []}

        profile = {
            "weight": weight,
            "height": height,
            "age": age,
            "daily_calorie_limit": daily_calorie_limit,
            "block_list": block_list,
        }
        self.save_profile(profile)
        return profile

    def save_profile(self, profile=None):
        if profile is None:
            profile = self.profile
        with open(self.profile_path, "w") as file:
            json.dump(profile, file)

    def update_profile(self):
        print("\nUpdating profile:")
        self.profile["weight"] = float(input("Enter your weight (kg): "))
        self.profile["height"] = float(input("Enter your height (cm): "))
        self.profile["age"] = int(input("Enter your age: "))
        self.profile["daily_calorie_limit"] = int(
            input("Set your daily calorie limit (kcal): ")
        )
        self.save_profile()
        print("Profile updated successfully.")

    def add_to_block_list(self):
        print("\nManage Block List:")
        print("1. Add Food to Block List")
        print("2. Add Category to Block List")
        choice = input("Choose an option: ")

        if choice == "1":
            food = input("Enter the food name to block: ").strip().lower()
            self.profile["block_list"]["foods"].append(food)
            print(f"'{food}' added to food block list.")
        elif choice == "2":
            category = input("Enter the category name to block: ").strip().lower()
            self.profile["block_list"]["categories"].append(category)
            print(f"'{category}' added to category block list.")
        else:
            print("Invalid choice.")
            return
        self.save_profile()

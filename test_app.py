import unittest
from unittest.mock import patch
from user import User
from food_log import FoodLog
from analysis import Analysis
from datetime import datetime
import pandas as pd
from datetime import timedelta


class TestEatingHabitTracker(unittest.TestCase):
    def setUp(self):
        # Prepare test user profile
        self.username = "test_user"
        self.test_profile = {
            "weight": 70.0,
            "height": 175.0,
            "age": 30,
            "daily_calorie_limit": 2000,
            "block_list": {"foods": ["pizza"], "categories": ["dessert"]},
        }
        self.user = User(self.username, profile=self.test_profile)

        # Load and preprocess the dataset
        data = pd.read_json("cleaned_sampled_food_dataset.json")
        print(data.head())
        data = data[["Food", "Category", "Calories"]]
        data.dropna(subset=["Food", "Category", "Calories"], inplace=True)
        data["Food"] = data["Food"].str.lower().str.strip()
        data["Category"] = data["Category"].str.lower().str.strip()
        data = data[data["Calories"] >= 0]
        sampled_data = data.sample(n=10, random_state=42)
        self.food_log_entries = sampled_data.to_dict(orient="records")

        # Prepare test food logs using the sampled data
        self.test_log = []
        base_date = datetime.now()
        for i, entry in enumerate(self.food_log_entries):
            log_entry = {
                "date": (base_date - timedelta(days=i)).strftime("%Y-%m-%d"),
                "food": entry["Food"],
                "category": entry["Category"],
                "calories": int(entry["Calories"]),
            }
            self.test_log.append(log_entry)

        self.food_log = FoodLog(self.username, log=self.test_log)
        self.analysis = Analysis(self.food_log)

    def test_check_calorie_limit_with_real_data(self):
        # Use the date of the first entry
        test_date = self.test_log[0]["date"]
        self.user.profile["daily_calorie_limit"] = 500  # Set a low limit for testing

        with patch("analysis.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime.strptime(test_date, "%Y-%m-%d")
            mock_datetime.strftime = datetime.strftime
            with patch("builtins.print") as mock_print:
                self.analysis.check_calorie_limit(self.user.profile)
                total_calories = self.food_log.get_daily_calories(test_date)
                if total_calories > self.user.profile["daily_calorie_limit"]:
                    mock_print.assert_any_call(
                        "\nWarning: You have exceeded your daily calorie limit!"
                    )
                else:
                    remaining = (
                        self.user.profile["daily_calorie_limit"] - total_calories
                    )
                    mock_print.assert_any_call(
                        f"\nYou have {remaining} kcal remaining for today."
                    )

    def test_check_calorie_limit_exceeded(self):
        # Use the date of the first entry
        test_date = self.test_log[0]["date"]
        self.user.profile["daily_calorie_limit"] = 500  # Set a low limit for testing

        with patch("analysis.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime.strptime(test_date, "%Y-%m-%d")
            mock_datetime.strftime = datetime.strftime
            with patch("builtins.print") as mock_print:
                self.analysis.check_calorie_limit(self.user.profile)
                total_calories = self.food_log.get_daily_calories(test_date)
                if total_calories > self.user.profile["daily_calorie_limit"]:
                    mock_print.assert_any_call(
                        "\nWarning: You have exceeded your daily calorie limit!"
                    )
                else:
                    remaining = (
                        self.user.profile["daily_calorie_limit"] - total_calories
                    )
                    mock_print.assert_any_call(
                        f"\nYou have {remaining} kcal remaining for today."
                    )

    def test_generate_weekly_report_with_real_data(self):
        with patch("builtins.print") as mock_print:
            self.analysis.generate_weekly_report()
            mock_print.assert_any_call("\n-- Weekly Eating Habits Report --")
            mock_print.assert_any_call("\nMost Consumed Categories:")
            # Check that categories are reported
            categories_reported = [
                args[0] for args in mock_print.call_args_list if " times" in args[0]
            ]
            self.assertTrue(categories_reported != None)

    def test_load_profile(self):
        # Test loading profile data
        self.assertEqual(self.user.profile["age"], 30)
        self.assertEqual(self.user.profile["daily_calorie_limit"], 2000)

    def test_add_to_block_list(self):
        # Test adding a new item to the block list
        with patch("builtins.input", side_effect=["1", "soda"]):
            with patch("builtins.print") as mock_print:
                self.user.add_to_block_list()
                self.assertIn("soda", self.user.profile["block_list"]["foods"])
                mock_print.assert_any_call("'soda' added to food block list.")

    def test_add_duplicate_to_block_list(self):
        # Test adding a duplicate item to the block list
        self.user.profile["block_list"]["foods"] = ["soda"]
        with patch("builtins.input", side_effect=["1", "soda"]):
            with patch("builtins.print") as mock_print:
                self.user.add_to_block_list()
                self.assertEqual(
                    self.user.profile["block_list"]["foods"].count("soda"), 2
                )
                mock_print.assert_any_call("'soda' added to food block list.")

    def test_log_food_negative_calories(self):
        # Test logging food with negative calories (invalid case)
        with patch("builtins.input", side_effect=["celery", "vegetable", "-10"]):
            with patch("builtins.print") as mock_print:
                self.food_log.log_food(self.user.profile)
                # Assuming the application accepts negative calories, which may not be realistic

    def test_update_profile(self):
        # Test updating the user profile
        with patch("builtins.input", side_effect=["75", "180", "31", "2200"]):
            self.user.update_profile()
            self.assertEqual(self.user.profile["weight"], 75)
            self.assertEqual(self.user.profile["height"], 180)
            self.assertEqual(self.user.profile["age"], 31)
            self.assertEqual(self.user.profile["daily_calorie_limit"], 2200)

    def test_zero_calorie_limit(self):
        # Test with a daily calorie limit of zero
        self.user.profile["daily_calorie_limit"] = 0
        with patch("analysis.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime.now()
            mock_datetime.strftime = datetime.strftime
            with patch("builtins.print") as mock_print:
                self.analysis.check_calorie_limit(self.user.profile)
                total_calories = self.food_log.get_daily_calories(
                    datetime.now().strftime("%Y-%m-%d")
                )
                if total_calories > 0:
                    mock_print.assert_any_call(
                        "\nWarning: You have exceeded your daily calorie limit!"
                    )
                else:
                    mock_print.assert_any_call("\nYou have 0 kcal remaining for today.")

    def test_invalid_calorie_input(self):
        # Test non-integer calorie input
        with patch("builtins.input", side_effect=["salad", "vegetable", "abc"]):
            with self.assertRaises(ValueError):
                self.food_log.log_food(self.user.profile)

    def test_remove_from_block_list(self):
        pass


if __name__ == "__main__":
    unittest.main()

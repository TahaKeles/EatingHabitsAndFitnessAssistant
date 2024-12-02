from collections import Counter
from datetime import datetime
import openai
import os

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


class Analysis:
    def __init__(self, food_log):
        self.food_log = food_log

    def check_calorie_limit(self, user_profile):
        date_str = datetime.now().strftime("%Y-%m-%d")
        total_calories = self.food_log.get_daily_calories(date_str)
        limit = user_profile["daily_calorie_limit"]
        if total_calories > limit:
            print("\nWarning: You have exceeded your daily calorie limit!")
        else:
            remaining = limit - total_calories
            print(f"\nYou have {remaining} kcal remaining for today.")

    def generate_weekly_report(self):
        logs = self.food_log.get_logs_in_date_range()  # Changed from get_weekly_logs()
        if not logs:
            print("\nNo data available for the report.")
            return

        categories = [entry["category"] for entry in logs]
        foods = [entry["food"] for entry in logs]

        category_counts = Counter(categories)
        food_counts = Counter(foods)

        print("\n-- Weekly Eating Habits Report --")
        print("\nMost Consumed Categories:")
        for category, count in category_counts.most_common():
            print(f"{category}: {count} times")

        print("\nMost Consumed Foods:")
        for food, count in food_counts.most_common():
            print(f"{food}: {count} times")

    def generate_gym_schedule(self, user_profile):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a fitness expert."},
                {
                    "role": "user",
                    "content": f"Create a gym schedule for this profile: {user_profile}",
                },
            ],
            max_tokens=150,
        )
        schedule = response.choices[0].message["content"]
        print("Generated Gym Schedule:")
        print(schedule)

        # Ask for user confirmation or modifications
        user_input = (
            input("\nWould you like to modify this schedule? (yes/no): ")
            .strip()
            .lower()
        )
        if user_input == "yes":
            modification_prompt = input(
                "Describe your preferred modifications: "
            ).strip()
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a fitness expert."},
                    {
                        "role": "user",
                        "content": f"Create a gym schedule for this profile: {user_profile}. Adjust as follows: {modification_prompt}",
                    },
                ],
                max_tokens=150,
            )
            schedule = response.choices[0].message["content"]
            print("Modified Gym Schedule:")
            print(schedule)

        return schedule

    def generate_eating_schedule(self, user_profile):
        # Extract recent food logs (past 7 days)
        recent_logs = self.food_log.get_logs_in_date_range()
        recent_logs_text = "\n".join(
            [
                f"- {log['date']}: {log['food']} ({log['calories']} kcal)"
                for log in recent_logs
            ]
        )

        # Construct the prompt
        prompt = f"""
        You are a nutrition expert. Based on the user's profile and their recent food intake logs, create a balanced eating schedule for them.

        User Profile:
        - Weight: {user_profile['weight']} kg
        - Height: {user_profile['height']} cm
        - Age: {user_profile['age']}
        - Daily Calorie Limit: {user_profile['daily_calorie_limit']} kcal
        - Blocked Foods: {', '.join(user_profile['block_list']['foods'])}
        - Blocked Categories: {', '.join(user_profile['block_list']['categories'])}

        Recent Food Intake:
        {recent_logs_text}

        Generate a detailed eating schedule for one day, ensuring the user stays within their calorie limit and avoids blocked foods and categories.
        """

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a nutrition expert."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
        )

        schedule = response.choices[0].message["content"]
        print("Generated Eating Schedule:")
        print(schedule)

        # Ask for user confirmation or modifications
        user_input = (
            input("\nWould you like to modify this schedule? (yes/no): ")
            .strip()
            .lower()
        )
        if user_input == "yes":
            modification_prompt = input(
                "Describe your preferred modifications: "
            ).strip()
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a nutrition expert."},
                    {
                        "role": "user",
                        "content": f"{prompt}\nAdjust as follows: {modification_prompt}",
                    },
                ],
                max_tokens=300,
            )
            schedule = response.choices[0].message["content"]
            print("Modified Eating Schedule:")
            print(schedule)

        return schedule

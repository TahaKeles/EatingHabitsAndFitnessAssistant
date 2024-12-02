from user import User
from food_log import FoodLog
from analysis import Analysis


def main():
    print("Welcome to Eating Habits and Fitness Assistant!")
    username = input("Enter your username: ").strip()
    user = User(username)
    food_log = FoodLog(username)
    analysis = Analysis(food_log)

    while True:
        print("\nMain Menu:")
        print("1. Update Profile")
        print("2. Manage Block List")
        print("3. Log Food Intake")
        print("4. Check Daily Calorie Status")
        print("5. Generate Weekly Report")
        print("6. Create Gym Schedule")  # New option for gym schedule
        print("7. Create Eating Schedule")  # New option for eating schedule
        print("8. Exit")  # Updated exit option
        choice = input("Choose an option: ")

        if choice == "1":
            user.update_profile()
        elif choice == "2":
            user.add_to_block_list()
        elif choice == "3":
            food_log.log_food(user.profile)
        elif choice == "4":
            analysis.check_calorie_limit(user.profile)
        elif choice == "5":
            analysis.generate_weekly_report()
        elif choice == "6":
            gym_schedule = analysis.generate_gym_schedule(user.profile)
            print("Generated Gym Schedule:")
            print(gym_schedule)
        elif choice == "7":
            eating_schedule = analysis.generate_eating_schedule(user.profile)
            print("Generated Eating Schedule:")
            print(eating_schedule)
        elif choice == "8":
            print("Thank you for using Eating Habits and Fitness Assistant. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

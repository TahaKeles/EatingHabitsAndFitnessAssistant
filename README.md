# Eating Habits and Fitness Assistant

A Python application that helps users track their eating habits, manage calorie intake, and generate personalized fitness recommendations using OpenAI's GPT-4.

## Features

- Track daily food intake and calories
- Set and monitor daily calorie limits
- Block specific foods and food categories
- Generate weekly eating habit reports
- Get AI-powered gym and eating schedules
- Unit test coverage for core functionality

## Requirements

- Python 3.7+
- Required packages listed in requirements.txt:
  - openai>=1.42.0
  - pytest>=7.0.0
  - python-dotenv>=1.0.0
  - pandas>=2.0.0
  - scikit-learn>=1.0.0
  - nltk>=3.8.0

## Installation

1. Clone this repository
2. Install dependencies: `bash
pip install -r requirements.txt   `

## Preprocessing

Before running the application, ensure that your dataset is preprocessed correctly. The preprocessing steps include:

1. **Loading the Dataset**: Load the JSON dataset using pandas.
2. **Cleaning Data**: Remove any rows with missing values in the `Food`, `Category`, or `Calories` columns.
3. **Standardizing Text**: Convert `Food` and `Category` fields to lowercase and strip any leading/trailing whitespace.
4. **Scaling Calories**: If necessary, scale the `Calories` values to appropriate units (e.g., from kilocalories to calories).

## Testing

To ensure the application functions correctly, run the unit tests provided. The tests cover various functionalities, including:

- Logging food intake
- Checking calorie limits
- Generating reports
- Managing block lists

To run the tests, use the following command:

python3 test_app.py

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import json


# File path to the large dataset
file_path = "en.openfoodfacts.org.products.csv"

# Define columns to retain
columns_to_keep = ["product_name", "main_category", "energy_100g"]

# Load dataset in chunks to handle large file size
chunk_size = 1000
relevant_data = []

print("Processing dataset in chunks...")

# Initialize counter and download required NLTK data
total_rows = 0
for chunk in pd.read_csv(
    file_path, sep="\t", usecols=columns_to_keep, chunksize=chunk_size, low_memory=False
):
    chunk = chunk.dropna(subset=columns_to_keep)
    chunk = chunk[chunk["energy_100g"] >= 0]
    relevant_data.append(chunk)

    # Keep track of total valid rows
    total_rows += len(chunk)

    # Stop if we have 10000 or more rows
    if total_rows >= 1000:
        break

# Combine all relevant chunks and take first 10000 rows
data = pd.concat(relevant_data)
data = data.head(1000)

# Further reduce the dataset size by sampling a smaller subset
data = data.sample(n=1000, random_state=42)  # Adjust n as needed

# Add some manually labeled test data
test_data = pd.DataFrame(
    {
        "product_name": [
            "Grilled Chicken Breast",
            "Brown Rice",
            "Salmon Fillet",
            "Sweet Potato",
            "Greek Yogurt",
            "Banana",
            "Almonds",
            "Quinoa",
            "Avocado",
            "Egg",
        ],
        "main_category": [
            "en:poultry",
            "en:grains",
            "en:fish",
            "en:vegetables",
            "en:dairy",
            "en:fruits",
            "en:nuts",
            "en:grains",
            "en:fruits",
            "en:eggs",
        ],
        "energy_100g": [
            165,  # calories per 100g
            112,
            208,
            86,
            59,
            89,
            579,
            120,
            160,
            155,
        ],
    }
)

# Append test data
data = pd.concat([data, test_data], ignore_index=True)

# Rename columns to align with application schema
data.rename(
    columns={
        "product_name": "Food",
        "main_category": "Category",
        "energy_100g": "Calories",
    },
    inplace=True,
)

# Normalize text columns
text_columns = ["Food", "Category"]
for col in text_columns:
    data[col] = data[col].str.lower().str.strip()

# Normalize numerical columns
scaler = MinMaxScaler()
data[["Calories"]] = scaler.fit_transform(data[["Calories"]])

# Save preprocessed dataset as CSV
cleaned_csv_path = "cleaned_sampled_food_dataset.csv"
data.to_csv(cleaned_csv_path, index=False)
print(f"Cleaned dataset saved as '{cleaned_csv_path}'")

# Save preprocessed dataset as JSON
cleaned_json_path = "cleaned_sampled_food_dataset.json"
data.to_json(cleaned_json_path, orient="records", indent=4)
print(f"Cleaned dataset saved as '{cleaned_json_path}'")

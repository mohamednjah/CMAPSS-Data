import pandas as pd

# Load the preprocessed dataset
df = pd.read_csv("data/preprocessed_data.csv")

# Display basic info
print("\n✅ Dataset Info:")
print(df.info())

# Display first rows
print("\n✅ First 5 rows:")
print(df.head())

# Check the shape of the dataset
print("\n✅ Final dataset shape:", df.shape)

# Check for missing values
print("\n✅ Missing values per column:")
print(df.isnull().sum())

# Display summary statistics
print("\n✅ Summary Statistics:")
print(df.describe())

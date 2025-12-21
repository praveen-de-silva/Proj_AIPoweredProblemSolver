import pandas as pd
from pymongo import MongoClient

# Paste your MongoDB Atlas connection string here
MONGO_URI = "mongodb+srv://pdsilva496_db_user:4jL8YCFoDnyfeFaY@couple-app.vxmmkoi.mongodb.net/?appName=couple-app"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["couple-app"]          # your database name
collection = db["problemlogs"]     # your collection name

# Fetch required fields only
data = list(collection.find(
    {},
    {"_id": 0, "text": 1, "predictedCategory": 1, "wasHelpful": 1}
))

# Convert to DataFrame
df = pd.DataFrame(data)

# Remove duplicate texts
df = df.drop_duplicates(subset="text")

try:
    # Save to CSV
    df.to_csv("dataset.csv", index=False)
    print(f"✅ Success! Exported {len(df)} unique records to dataset.csv")
except Exception as e:
    print(f"❌ Failed to export CSV: {e}")


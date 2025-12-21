import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib

# 1. Load the NEW dataset
print("⏳ Loading dataset...")
# We use 'header=0' because the first row contains "text,category"
df = pd.read_csv("dataset.csv")

# 2. Check the data
print(f"✅ Loaded {len(df)} examples.")
print(df.head())

# 3. Split into Input (X) and Output (y)
X = df['text']
y = df['category']

# 4. Create the AI Pipeline (The Brain)
# CountVectorizer: Turns words into numbers
# MultinomialNB: The math that finds patterns
# text → numbers → prediction
model = make_pipeline(CountVectorizer(), MultinomialNB()) 

# 5. Train the Model
print("🧠 Training the AI...")
model.fit(X, y)

# 6. Save the Model
joblib.dump(model, "couple_ai_model.pkl")
print("🎉 Success! Model saved as 'couple_ai_model.pkl'")

# --- OPTIONAL: TEST IT IMMEDIATELY ---
print("\n🔍 Testing with new sentences:")
test_sentences = [
    "He never helps with the cleaning",
    "The credit card bill is too high",
    "He ignores my texts all day",
    "I don't trust him anymore"
]
predictions = model.predict(test_sentences)

for text, pred in zip(test_sentences, predictions):
    print(f"📝 '{text}' -> 🤖 {pred}")
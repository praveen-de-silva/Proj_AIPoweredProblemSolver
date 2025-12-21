from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

# 1. Load the Trained Brain
# We load the model once when the server starts
try:
    model = joblib.load("couple_ai_model.pkl")
    print("✅ Brain Loaded: couple_ai_model.pkl")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# 2. Define the Advice Database
# The AI predicts the CATEGORY, but we still need to provide the ADVICE.
# We map the category names to specific helpful tips.
ADVICE_DB = {
    "Chores": [
        "Create a shared chore chart visible to both.",
        "Set a 15-minute timer to clean together with music.",
        "Agree on 'minimum standards' for cleanliness.",
        "Thank each other when a chore is done voluntarily."
    ],
    "Finances": [
        "Schedule a weekly 'money date' to review expenses calmly.",
        "Set a 'cooling-off' period (24hrs) for big purchases.",
        "Create a joint account for bills but keep personal spending money.",
        "Focus on shared goals (like a vacation) rather than debt."
    ],
    "Affection": [
        "Schedule a weekly date night (no phones allowed).",
        "Practice the '6-second kiss' rule when saying goodbye.",
        "Send a random appreciation text during the day.",
        "Ask 'How can I make you feel loved today?'"
    ],
    "General": [
        "Use 'I feel' statements instead of 'You always' statements.",
        "Take a 20-minute timeout if an argument gets too heated.",
        "Focus on listening to understand, not to reply.",
        "Remember you are on the same team against the problem."
    ]
}

class Problem(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "AI Brain is Active 🧠"}

@app.post("/predict")
def predict_problem(problem: Problem):
    if model is None:
        return {"category": "Error", "suggested_solutions": ["Model not loaded."]}

    # 1. Ask the Brain
    # The model expects a list of text, so we wrap input in []
    # It returns an array, so we take the first item [0]
    predicted_category = model.predict([problem.text])[0]

    # 2. Get Advice for that Category
    # If the AI predicts a weird category we don't know, fallback to "General"
    solutions = ADVICE_DB.get(predicted_category, ADVICE_DB["General"])

    return {
        "category": predicted_category,
        "suggested_solutions": solutions
    }
# classification.py

from fastapi import APIRouter
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification

classification_router = APIRouter()

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Define class labels
CLASS_LABELS = {
    0: "No Disorder",
    1: "Sleep Disorder",
    2: "Depression",
    # Add more labels as needed
}

class ClassificationRequest(BaseModel):
    texts: list[str]  # Adjust to handle multiple texts

@classification_router.post("/")
async def classify(request: ClassificationRequest):
    texts = request.texts
    results = []
    
    for text in texts:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        try:
            outputs = model(**inputs)
            logits = outputs.logits
            predicted_class = logits.argmax().item()
            class_label = CLASS_LABELS.get(predicted_class, "Unknown")
            results.append({"text": text, "predicted_class": predicted_class, "class_label": class_label})
        except Exception as e:
            return {"error": str(e)}
    
    return results

from fastapi import APIRouter
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

router = APIRouter()

# Initialize the model and tokenizer
model_name = "facebook/bart-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Directory containing the local articles
ARTICLES_DIR = os.getenv("ARTICLES_DIR", "articles")

class PromptRequest(BaseModel):
    prompt: str

def load_articles():
    articles = []
    for filename in os.listdir(ARTICLES_DIR):
        if filename.endswith(".txt"):
            with open(os.path.join(ARTICLES_DIR, filename), 'r') as file:
                content = file.read()
                articles.append({
                    "title": filename,
                    "content": content
                })
    return articles

@router.post("/")
async def rag(request: PromptRequest):
    prompt = request.prompt
    # Load articles from the local dataset
    articles = load_articles()
    
    # Combine article contents into a single string
    articles_text = " ".join(article['content'] for article in articles)
    
    # Tokenize prompt and articles
    inputs = tokenizer(prompt + " " + articles_text, return_tensors="pt", truncation=True, padding=True)
    
    # Check the input tensor size
    print(f"Input IDs: {inputs['input_ids']}")
    print(f"Attention Mask: {inputs['attention_mask']}")
    
    # Use the language model to generate a response based on the retrieved articles
    try:
        outputs = model.generate(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_length=150,
            num_beams=2,
            early_stopping=True
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        return {"error": str(e)}
    
    return {"response": response, "articles": [article['title'] for article in articles]}

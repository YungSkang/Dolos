from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# This model was fine-tuned specifically on URLs
MODEL_NAME = "pirocheto/phishing-url-detection"

_tokenizer = None
_model     = None

def _load_deep_model():
    global _tokenizer, _model
    if _tokenizer is None:
        print("Loading DistilBERT URL classifier from HuggingFace...")
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model     = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        _model.eval()
        print("Deep model loaded.")

def predict_url_deep(url: str) -> dict:
    _load_deep_model()

    inputs  = _tokenizer(url, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        logits = _model(**inputs).logits
    probs   = F.softmax(logits, dim=-1)[0]

    # Check model's label mapping
    id2label = _model.config.id2label
    scores   = {id2label[i]: float(probs[i]) for i in range(len(probs))}

    phishing_score = scores.get('phishing', scores.get('PHISHING', 0.0))

    return {
        'verdict':    'phishing' if phishing_score > 0.5 else 'legitimate',
        'confidence': round(phishing_score * 100, 1),
        'scores':     scores,
    }
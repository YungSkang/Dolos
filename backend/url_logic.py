import joblib
import pandas as pd
import os
from huggingface_hub import hf_hub_download
from backend.url_features import extract_features
from backend.url_apis import scan_url

REPO_ID   = "Skandaloso/URL_Phishing_Detection"
MODEL     = None
COLUMNS   = None
LABEL_MAP = None

CONFIDENCE_THRESHOLD = 0.75


def _load_model():
    global MODEL, COLUMNS, LABEL_MAP
    if MODEL is not None:
        return True  # already loaded, skip

    try:
        print("Downloading model from HuggingFace...")

        model_path    = hf_hub_download(repo_id=REPO_ID, filename="url_model.pkl")
        columns_path  = hf_hub_download(repo_id=REPO_ID, filename="url_features_columns.pkl")
        labelmap_path = hf_hub_download(repo_id=REPO_ID, filename="url_label_map.pkl")

        MODEL     = joblib.load(model_path)
        COLUMNS   = joblib.load(columns_path)
        LABEL_MAP = joblib.load(labelmap_path)

        print("Model loaded successfully.")
        return True

    except Exception as e:
        print(f"Failed to load model: {e}")
        return False


def analyze_url(url: str, use_virustotal: bool = True) -> dict:
    model_ready = _load_model()
    features    = extract_features(url)

    if model_ready:
        features_df     = pd.DataFrame([features]).reindex(columns=COLUMNS, fill_value=0)
        predicted_label = MODEL.predict(features_df)[0]
        proba           = MODEL.predict_proba(features_df)[0]
        classes         = list(MODEL.classes_)

        phishing_idx = classes.index(LABEL_MAP['phishing_label'])
        confidence   = float(proba[phishing_idx])
        is_phishing  = predicted_label == LABEL_MAP['phishing_label']
        ml_verdict   = 'phishing' if is_phishing else 'legitimate'
    else:
        ml_verdict  = 'unavailable'
        confidence  = 0

    result = {
        'url':           url,
        'ml_verdict':    ml_verdict,
        'confidence':    round(confidence * 100, 1),
        'features':      features,
        'vt_result':     None,
        'final_verdict': ml_verdict,
    }

    # Always call VirusTotal — show both results to user
    if use_virustotal:
        vt = scan_url(url)
        result['vt_result'] = vt

        if vt.get('verdict') == 'malicious':
            result['final_verdict'] = 'phishing'
        elif vt.get('verdict') == 'clean':
            result['final_verdict'] = 'legitimate'
        else:
            result['final_verdict'] = ml_verdict

    return result
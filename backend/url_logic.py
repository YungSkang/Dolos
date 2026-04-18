import joblib
import pandas as pd
import os
from backend.url_features import extract_features
from backend.url_apis import scan_url

# Load model once at startup
MODEL   = joblib.load(os.path.join(os.path.dirname(__file__), 'url_model.pkl'))
COLUMNS = joblib.load(os.path.join(os.path.dirname(__file__), 'url_features_columns.pkl'))
LABEL_MAP = joblib.load(os.path.join(os.path.dirname(__file__), 'url_label_map.pkl'))

# confidence threshold, below this we call VirusTotal API
CONFIDENCE_THRESHOLD = 0.75


def _load_model():
    global MODEL, COLUMNS, LABEL_MAP
    if MODEL is None:
        model_path    = os.path.join(os.path.dirname(__file__), 'url_model.pkl')
        columns_path  = os.path.join(os.path.dirname(__file__), 'url_features_columns.pkl')
        labelmap_path = os.path.join(os.path.dirname(__file__), 'url_label_map.pkl')
        if os.path.exists(model_path):
            MODEL     = joblib.load(model_path)
            COLUMNS   = joblib.load(columns_path)
            LABEL_MAP = joblib.load(labelmap_path)
        else:
            return False
    return True

def analyze_url(url: str, use_virustotal: bool = True) -> dict:
    # Layer 1 — ML model
    features    = extract_features(url)
    features_df = pd.DataFrame([features]).reindex(columns=COLUMNS, fill_value=0)
    
    # --- YOUR NEW LOGIC HERE ---
    predicted_label = MODEL.predict(features_df)[0]
    proba           = MODEL.predict_proba(features_df)[0]
    classes         = MODEL.classes_  
    
    phishing_idx    = list(classes).index(LABEL_MAP['phishing_label'])
    confidence      = float(proba[phishing_idx])
    is_phishing     = predicted_label == LABEL_MAP['phishing_label']
    
    ml_verdict  = 'phishing' if is_phishing else 'legitimate'
    # ---------------------------

    result = {
        'url':        url,
        'ml_verdict': ml_verdict,
        'confidence': round(confidence * 100, 1),
        'features':   features,
        'vt_result':  None,
    }

    # Always call VirusTotal when enabled — show both results to user
    if use_virustotal:
        vt = scan_url(url)
        result['vt_result'] = vt

        # VT overrides ML only when it has a strong signal
        if vt.get('verdict') == 'malicious':
            result['final_verdict'] = 'phishing'
        elif vt.get('verdict') == 'clean':
            result['final_verdict'] = 'legitimate'
        else:
            result['final_verdict'] = ml_verdict
    else:
        result['final_verdict'] = ml_verdict

    return result
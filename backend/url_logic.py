import joblib
import pandas as pd
import os
from huggingface_hub import hf_hub_download
from backend.url_features import extract_features, is_trusted
from backend.url_apis import scan_url
from backend.url_deep_model import predict_url_deep

REPO_ID   = "Skandaloso/URL_Phishing_Detection"
MODEL     = None
COLUMNS   = None
LABEL_MAP = None

PHISHING_THRESHOLD = 0.65  # raised from 0.50 to reduce false positives


def _load_model():
    global MODEL, COLUMNS, LABEL_MAP
    if MODEL is not None:
        return True

    base_dir      = os.path.dirname(__file__)
    model_path    = os.path.join(base_dir, 'url_model.pkl')
    columns_path  = os.path.join(base_dir, 'url_features_columns.pkl')
    labelmap_path = os.path.join(base_dir, 'url_label_map.pkl')

    try:
        if os.path.exists(model_path):
            print("Loading RF model from local files...")
            MODEL     = joblib.load(model_path)
            COLUMNS   = joblib.load(columns_path)
            LABEL_MAP = joblib.load(labelmap_path)
        else:
            token         = os.getenv('HUGGINGFACE_TOKEN')
            model_path    = hf_hub_download(repo_id=REPO_ID, filename="url_model.pkl",            token=token)
            columns_path  = hf_hub_download(repo_id=REPO_ID, filename="url_features_columns.pkl", token=token)
            labelmap_path = hf_hub_download(repo_id=REPO_ID, filename="url_label_map.pkl",        token=token)
            MODEL     = joblib.load(model_path)
            COLUMNS   = joblib.load(columns_path)
            LABEL_MAP = joblib.load(labelmap_path)
        return True
    except Exception as e:
        print(f"RF model load failed: {e}")
        return False


def _weighted_verdict(rf_phishing: float, deep_phishing: float) -> tuple:
    """
    Combine RF and deep model scores with weights.
    RF is more reliable on structural features.
    Deep model is better at semantic/character patterns.
    """
    combined = (rf_phishing * 0.45) + (deep_phishing * 0.55)
    verdict  = 'phishing' if combined > PHISHING_THRESHOLD else 'legitimate'
    return verdict, round(combined * 100, 1)


def analyze_url(url: str, use_virustotal: bool = True) -> dict:
    features = extract_features(url)

    #0: Trusted domain whitelist
    if is_trusted(url):
        result = {
            'url':            url,
            'final_verdict':  'legitimate',
            'ml_verdict':     'legitimate',
            'deep_verdict':   'legitimate',
            'confidence':     100.0,
            'trusted_domain': True,
            'features':       features,
            'vt_result':      None,
        }
        if use_virustotal:
            result['vt_result'] = scan_url(url)
        return result

    # 1: Random Forest
    rf_verdict    = 'unavailable'
    rf_confidence = 0.0

    if _load_model():
        features_df     = pd.DataFrame([features]).reindex(columns=COLUMNS, fill_value=0)
        predicted_label = MODEL.predict(features_df)[0]
        proba           = MODEL.predict_proba(features_df)[0]
        classes         = list(MODEL.classes_)
        phishing_idx    = classes.index(LABEL_MAP['phishing_label'])
        rf_confidence   = float(proba[phishing_idx])
        rf_verdict      = 'phishing' if rf_confidence > PHISHING_THRESHOLD else 'legitimate'

    # 2: DistilBERT deep model
    try:
        deep_result    = predict_url_deep(url)
        deep_verdict   = deep_result['verdict']
        deep_confidence = deep_result['confidence'] / 100
    except Exception as e:
        print(f"Deep model error: {e}")
        deep_verdict    = 'unavailable'
        deep_confidence = rf_confidence  # fall back to RF score

    # Combine Layer 1 + Layer 2
    if rf_verdict != 'unavailable' and deep_verdict != 'unavailable':
        final_ml, combined_confidence = _weighted_verdict(rf_confidence, deep_confidence)
    elif rf_verdict != 'unavailable':
        final_ml, combined_confidence = rf_verdict, round(rf_confidence * 100, 1)
    else:
        final_ml, combined_confidence = deep_verdict, round(deep_confidence * 100, 1)

    result = {
        'url':             url,
        'ml_verdict':      rf_verdict,
        'deep_verdict':    deep_verdict,
        'confidence':      combined_confidence,
        'trusted_domain':  False,
        'features':        features,
        'vt_result':       None,
        'final_verdict':   final_ml,
    }

    #3: VirusTotal
    if use_virustotal:
        vt = scan_url(url)
        result['vt_result'] = vt

        # VT has the final word when it has a strong signal
        if vt.get('verdict') == 'malicious':
            result['final_verdict'] = 'phishing'
        elif vt.get('verdict') == 'clean' and final_ml == 'phishing' and combined_confidence < 80:
            # VT says clean AND ML wasn't very confident → trust VT
            result['final_verdict'] = 'legitimate'

    return result
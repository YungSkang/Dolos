import requests
import hashlib
import base64
import os
import time

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

VT_API_KEY = os.getenv('VIRUSTOTAL_API_KEY')
VT_BASE    = 'https://www.virustotal.com/api/v3'


HEADERS = {
    'x-apikey': VT_API_KEY,
    'accept':   'application/json',
}

#VirusTotal identifies URLs by base64-encoded form

def _url_id(url: str) -> str:
    return base64.urlsafe_b64encode(url.encode()).decode().rstrip('=')

#submit URL for scanning and return analysis results
def scan_url(url: str) -> dict:
    headers = {
        'x-apikey': os.getenv('VIRUSTOTAL_API_KEY'),
        'accept':   'application/json',
    }
    # Step 1 — submit the URL
    submit_res = requests.post(
        f'{VT_BASE}/urls',
        headers=HEADERS,
        data={'url': url},
        timeout=10
    )
    if submit_res.status_code != 200:
        print(VT_API_KEY)
        return {'error': 'Failed to submit URL to VirusTotal'}

    # Step 2 — wait briefly then fetch the report
    time.sleep(2)
    url_id     = _url_id(url)
    report_res = requests.get(
        f'{VT_BASE}/urls/{url_id}',
        headers=HEADERS,
        timeout=10
    )

    if report_res.status_code != 200:
        return {'error': 'Failed to retrieve VirusTotal report'}

    data  = report_res.json()
    stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})

    malicious  = stats.get('malicious', 0)
    suspicious = stats.get('suspicious', 0)
    harmless   = stats.get('harmless', 0)
    total      = sum(stats.values()) or 1

    return {
        'malicious':   malicious,
        'suspicious':  suspicious,
        'harmless':    harmless,
        'total':       total,
        'verdict':     (
            'malicious'  if malicious > 2 else
            'suspicious' if malicious > 0 or suspicious > 2 else
            'clean'
        ),
        'summary': f'{malicious}/{total} engines flagged this URL as malicious'
    }



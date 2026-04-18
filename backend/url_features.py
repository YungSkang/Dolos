import re
import tldextract
import urllib.parse

# Suspicious keywords commonly found in phishing URLs
SUSPICIOUS_KEYWORDS = [
    'login', 'verify', 'secure', 'update', 'account', 'banking',
    'confirm', 'password', 'credential', 'suspend', 'unusual',
    'signin', 'authenticate', 'validation', 'recover', 'unlock'
]

# Known URL shorteners — attackers use these to hide real destinations
URL_SHORTENERS = [
    'bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly',
    'buff.ly', 'rebrand.ly', 'cutt.ly', 'shorturl.at'
]

def extract_features(url: str) -> dict:
    parsed   = urllib.parse.urlparse(url)
    ext      = tldextract.extract(url)
    hostname = parsed.netloc or ''
    path     = parsed.path or ''
    full_url = url.lower()

    features = {
        # Length features — phishing URLs tend to be longer
        'url_length':          len(url),
        'hostname_length':     len(hostname),
        'path_length':         len(path),

        # Dot and subdomain count — many subdomains = suspicious
        'dot_count':           url.count('.'),
        'subdomain_count':     len(ext.subdomain.split('.')) if ext.subdomain else 0,

        # Special character counts
        'hyphen_count':        url.count('-'),
        'at_sign':             int('@' in url),       # @symbol tricks browsers
        'double_slash':        int('//' in path),     # redirect trick
        'question_mark_count': url.count('?'),
        'ampersand_count':     url.count('&'),
        'percent_count':       url.count('%'),        # URL encoding abuse

        # Protocol
        'has_https':           int(parsed.scheme == 'https'),
        'has_http':            int(parsed.scheme == 'http'),

        # IP address instead of domain — major red flag
        'has_ip_address':      int(bool(re.match(
            r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', hostname
        ))),

        # Suspicious patterns
        'has_suspicious_keyword': int(any(k in full_url for k in SUSPICIOUS_KEYWORDS)),
        'is_url_shortener':       int(any(s in hostname for s in URL_SHORTENERS)),
        'has_port':               int(bool(parsed.port)),
        'tld_length':             len(ext.suffix) if ext.suffix else 0,

        # Digit ratio in domain — e.g. paypa1.com
        'digit_ratio_in_domain':  (
            sum(c.isdigit() for c in ext.domain) / len(ext.domain)
            if ext.domain else 0
        ),
    }

    return features
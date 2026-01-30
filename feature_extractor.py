# feature_extractor.py
import re
from urllib.parse import urlparse

# ---------------------------------
# URL VALIDATION FUNCTION
# ---------------------------------
def is_valid_url(url):
    pattern = re.compile(
        r'^(https?:\/\/)?'          # http or https (optional)
        r'([a-zA-Z0-9-]+\.)+'       # domain name
        r'[a-zA-Z]{2,}'             # top-level domain
        r'(\/.*)?$'                 # path (optional)
    )
    return re.match(pattern, url) is not None


# ---------------------------------
# FEATURE EXTRACTION
# ---------------------------------
def extract_features(url):

    # ❌ Reject invalid URLs
    if not is_valid_url(url):
        return None

    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    features = {}

    features['url_length'] = len(url)
    features['num_dots'] = url.count('.')
    features['has_ip'] = int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url)))
    features['has_https'] = int(url.startswith('https'))
    features['num_hyphens'] = url.count('-')

    # Subdomain count safely handled
    if domain:
        features['num_subdomains'] = max(0, len(domain.split('.')) - 2)
    else:
        features['num_subdomains'] = 0

    return features

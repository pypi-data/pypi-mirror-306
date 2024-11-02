from .apachelm import ApacheHelm

def lmclient(api_key, model="apachelm-v3"):
    """Creates an instance of ApacheHelm with the given API key and model."""
    return ApacheHelm(api_key=api_key, model=model)

__version__ = "0.1.0"

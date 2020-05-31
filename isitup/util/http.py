# Import modules
import requests
from fake_useragent import UserAgent


def download_something(domain, path=None, token=None, port=443, ssl=True):
    """Download some thing from the web

    Attempt to download all content of a web page

    Args:
        domain: A domain
        path: A path to download on said domain. Start string with "/". Default None
        token: Matrix access token. Default None
        port: Port to connect on. Default 443
        ssl: Use HTTPS? Default True

    Returns:
        Downloaded content or None if error
    """

    # Set a random valid user-agent
    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    # Create URL
    if ssl:
        url = f'https://{domain}'
    else:
        url = f'http://{domain}'
    
    if port:
        url += f':{port}'
    
    if path:
        url += path

    # Try and download
    try:
        http_request = requests.get(url, headers=headers, timeout=1)
    except Exception:
        return(None)

    # If not 200
    if not http_request.status_code == 200:
        return(None)
    
    return(http_request.content.decode('utf-8'))


def send_email():
    """Send an email
    
    TODO:
        - Add email config to config.ini
        - send email
    """
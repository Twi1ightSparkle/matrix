# Import modules
import base64
import hashlib
from . import http


def b64(content, encode=True):
    """Encode/Decode string to/from base64

    Checks if content is base64 or not. Then converts it to or from base64.

    Args:
        content: Content to encode or decode
        encode: Encode or decode content. Default True (encode string to base64)
    
    Returns:
        The encoded/decoded message
    """

    if encode:
        content_bytes = content.encode('ascii')
        base64_bytes = base64.b64encode(content_bytes)
        base64_content = base64_bytes.decode('ascii')
        return base64_content
    else:
        base64_bytes = content.encode('ascii')
        content_bytes = base64.b64decode(base64_bytes)
        message = content_bytes.decode('ascii')
        return message


def check_media(url):
    """Check if something is available or has a new hash

    Checks if url is available, uf yes, download and hash it, then see if it has changed

    Args:
        url: A complete url to something
    
    Returns:
        0 if available and no change.
        1 if not available.
        2 if it has changed
    """

    media = http.download_something(url):

    # If failed to download
    if not media:
        return 1
    
    # Hash media
    hashed_media = hashlib.sha512(media).hexdigest()







def check_static_content():
    """Check if static content has changed

    TODO:
        - check if content has been checked before
        - if no, save to db
        - if yes, compare to db
        - if no change, log all ok
        - if changed, log change and email
    """
    
    

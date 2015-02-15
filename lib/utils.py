"""
Utility functions
"""

from hashlib import md5
from urllib import urlencode


def gravatar_url(email, size=150):
    hasher = md5()
    hasher.update(email.strip().lower())
    return "/".join(["https://www.gravatar.com/avatar",
                     hasher.hexdigest()+"?"+urlencode({"s": size, "d": "identicon"})])


def gravatar_profile(email):
    hasher = md5()
    hasher.update(email.strip().lower())
    return "/".join(["https://www.gravatar.com", hasher.hexdigest()])


def header_to_blobkey(header):
    headers = header.split(";")
    for entry in headers:
        if "blob-key" in entry:
            return entry.split("\"")[1]
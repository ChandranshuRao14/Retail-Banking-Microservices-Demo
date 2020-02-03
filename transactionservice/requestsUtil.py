import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def make_request_session(requiredStatusCodes, tries=5, backoff_factor=1):
    session = requests.Session()
    retries = Retry(
        total=tries,
        backoff_factor=backoff_factor,
        status_forcelist=tuple(
            x
            for x in requests.status_codes._codes
            if x not in requiredStatusCodes
        ),
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

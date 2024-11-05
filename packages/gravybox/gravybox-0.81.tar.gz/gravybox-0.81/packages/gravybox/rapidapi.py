import os

from gravybox.betterstack import collect_logger
from gravybox.exceptions import BadStatusCode
from gravybox.requests import AsyncRequestManager

logger = collect_logger()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")


async def query_rapidapi(host, endpoint, query, extra_headers=None):
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": host
    }
    if extra_headers is not None:
        headers |= extra_headers
    url = f"https://{host}/{endpoint}"
    response = await AsyncRequestManager.client().get(url, headers=headers, params=query, follow_redirects=True)
    if response.status_code == 200:
        return response.json()
    else:
        raise BadStatusCode(response)

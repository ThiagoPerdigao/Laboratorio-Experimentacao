import requests
import time

def rest_request(url: str, headers: dict):
    start = time.time()
    response = requests.get(url, headers=headers)
    end = time.time()

    duration_ms = (end - start) * 1000
    size_bytes = len(response.content) + sum(len(k)+len(v) for k, v in response.headers.items())

    return duration_ms, size_bytes, response.status_code

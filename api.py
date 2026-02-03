import requests

API_URL = "http://127.0.0.1:8000"
TOKEN = "kustosze"


def fetch_results():
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    response = requests.get(
        f"{API_URL}/results",
        headers=headers,
        timeout=5
    )
    response.raise_for_status()
    return response.json()

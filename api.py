import requests
import json



with open('credentials.json','r',encoding='utf-8') as file:
    data = json.load(file)

API_URL = data['api_url']
TOKEN = data['api_token']


def fetch_results():
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    response = requests.get(
        f"{API_URL}/results",
        headers=headers,
        timeout=60
    )
    response.raise_for_status()
    return response.json()

def fetch_quali_results():
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    response = requests.get(
        f"{API_URL}/quali_results",
        headers=headers,
        timeout=60
    )
    response.raise_for_status()
    return response.json()


def get_driver_list(season: int):
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    response = requests.get(
        f"{API_URL}/drivers_in_season_{season}",
        headers=headers,
        timeout=60
    )
    response.raise_for_status()
    return response.json()

def get_driver_stats_race(season: int, driver: str):
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    response = requests.get(
        f"{API_URL}/driver-stats-races/{season}/{driver}",
        headers=headers,
        timeout=60
    )
    response.raise_for_status()
    return response.json()

def get_driver_stats_quali(season: int, driver: str):
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    response = requests.get(
        f"{API_URL}/driver-stats-qualis/{season}/{driver}",
        headers=headers,
        timeout=60
    )
    response.raise_for_status()
    return response.json()
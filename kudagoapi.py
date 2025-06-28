
import aiohttp
from datetime import datetime

BASE_URL = "https://kudago.com/public-api/v1.4"

async def get_cinema_events(city: str, date: str):
    start = int(datetime.strptime(date, "%Y-%m-%d").timestamp())
    end = start + 86400

    url = f"{BASE_URL}/events/"
    params = {
        "location": city,
        "actual_since": start,
        "actual_until": end,
        "categories": "cinema",
        "fields": "title,place",
        "page_size": 10
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                return (await resp.json()).get("results", [])
            return []

# request_handler.py
"""
Request generation and simulation for FloodPulse.
"""

import random
import time
from faker import Faker
from aiohttp import ClientSession, ClientTimeout
from proxy_manager import ProxyPool

fake = Faker()

def random_request() -> tuple[str, dict]:
    """Generates a random HTTP request for FloodPulse."""
    path = f"/page{random.randint(1, 1000)}"
    headers = {
        "User-Agent": fake.user_agent(),
        "Accept": random.choice(["text/html", "*/*", "application/json"]),
        "X-Forwarded-For": fake.ipv4(),
        "Accept-Language": random.choice(["en-US", "fr-FR", "de-DE"]),
        "Referer": f"https://{fake.domain_name()}/"
    }
    return path, headers

async def fetch(session: ClientSession, url: str, proxy_pool: ProxyPool, proxy: str):
    """Simulates a single request for FloodPulse."""
    start = time.time()
    path, headers = random_request()
    try:
        async with session.get(f"{url}{path}", headers=headers, proxy=f"http://{proxy}" if proxy != "direct" else None, timeout=ClientTimeout(total=5)) as resp:
            await resp.text()
            latency = time.time() - start
            proxy_pool.update(proxy, True, latency)
    except Exception as e:
        print(f"Request to {url}{path} via {proxy} failed: {str(e)}")
        proxy_pool.update(proxy, False, time.time() - start)
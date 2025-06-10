# FloodPulse

FloodPulse is a Python-based tool designed to simulate high-volume HTTP traffic for penetration testing server resilience. It combines controlled bursts of requests with proxy rotation and realistic traffic patterns to stress-test servers, ideal for evaluating systems capable of handling massive user loads. If proxy fetching fails, it falls back to direct connections for uninterrupted testing. Recent updates optimize it to send significantly more requests within the test duration.

**WARNING: Use FloodPulse only on servers you own or have explicit, written authorization to test. Unauthorized or illegal use, such as targeting systems without permission, may violate laws (e.g., the Computer Fraud and Abuse Act in the U.S., the Computer Misuse Act in the U.K., or the Indian Information Technology Act, 2000) and result in severe legal consequences. Ensure all usage complies with applicable laws and ethical standards.**

## Features
- Scales to 100K+ requests with 10K concurrent users by default, with optimizations for even higher volumes.
- Smart proxy rotation with performance tracking (falls back to direct connection if no proxies are available).
- Randomized request paths and headers for realistic simulation.
- User-defined target URL at runtime with automatic HTTPS detection for port 443.

## Prerequisites
- Python 3.8+
- Dependencies: `aiohttp`, `requests`, `faker` (see `requirements.txt`)

## Installation
1. Clone or download this repository:
   ```bash
   git clone https://github.com/Gaurav5091/FloodPulse
   cd FloodPulse

    Create and activate a virtual environment (recommended, especially on systems like Kali Linux):
    bash

python3 -m venv venv
source venv/bin/activate
Install dependencies:
bash

    pip install -r requirements.txt

## Usage

Run FloodPulse and provide the target URL when prompted:
bash
python floodpulse.py

Example input: https://example.com:443 or example.com:443 (automatically uses HTTPS for port 443).
Configuration

Edit config.py to adjust:

    NUM_REQUESTS: Total requests to attempt (default: 100,000).
    CONCURRENT_USERS: Max concurrent requests before batching (default: 10,000).
    TEST_DURATION: Test duration in seconds (default: 60).
    PROXY_API_URL: Proxy source (default: https://www.sslproxies.org/; replace with a paid API for better reliability).

## Changes for Higher Request Volume

Recent updates maximize the number of requests sent within the test duration:

    Removed Request Delay: The asyncio.sleep(random.uniform(0.1, 1.0)) delay between requests was removed, previously limiting throughput to ~100 requests in 60 seconds (due to an average 0.55-second delay). Now, requests are sent as fast as possible, constrained only by server response time and concurrency limits.
    Smaller Batch Size: The run_test() function now batches requests at 100 instead of waiting for 10,000 (CONCURRENT_USERS), triggering asyncio.gather() more frequently. This increases concurrency within the 60-second TEST_DURATION, allowing thousands to tens of thousands of requests.
    HTTPS Default for 443: If the input includes :443 without a protocol, it defaults to https://, fixing protocol mismatches that caused request failures (e.g., "Server disconnected").

## Impact

    Before: With delays, only ~100 requests were sent in 60 seconds.
    After: Without delays and with a batch size of 100, it can send 10,000–50,000+ requests in 60 seconds, depending on server response and network conditions.
    Tuning: Increase TEST_DURATION (e.g., to 600 seconds) or lower the batch size further (e.g., to 10) in floodpulse.py to approach NUM_REQUESTS = 100,000.

## Example Output
text
Welcome to FloodPulse!
Enter the target URL (e.g., http://example.com:80): webfreakz.in:443
FloodPulse targeting: https://webfreakz.in:443
Fetching proxies for FloodPulse...
No proxies found; using direct connection as fallback.
FloodPulse filtered to 1 working proxies.
FloodPulse test complete in 60.05s. Sent 50000 requests to https://webfreakz.in:443.
Proxy direct: 49800 successes, 200 fails, avg latency 0.12s
Scaling to 1M Users

## For massive tests (e.g., 1M requests or users):

    Increase NUM_REQUESTS and TEST_DURATION in config.py (e.g., NUM_REQUESTS = 1000000, TEST_DURATION = 600).
    Lower the batch size in floodpulse.py (e.g., replace if len(tasks) >= 100 with if len(tasks) >= 10).
    Distribute across multiple instances using multiprocessing or cloud services.
    Use a paid proxy service (e.g., Oxylabs, Smartproxy) for reliable IPs instead of the default free proxy source.

## Legal Notice

FloodPulse is intended solely for legitimate penetration testing and server resilience evaluation by authorized users. Use this tool only on systems you own or have explicit, written permission to test. Unauthorized use, including targeting systems without consent, may violate local, national, or international laws (e.g., the Computer Fraud and Abuse Act in the U.S., the Computer Misuse Act in the U.K., or the Indian Information Technology Act, 2000), as well as terms of service of networks or proxy providers. The developers of FloodPulse are not responsible for any misuse, damages, or legal consequences resulting from improper use of this tool. Always ensure compliance with applicable laws and ethical guidelines before running FloodPulse.
## License

FloodPulse is licensed under the MIT License. See the  file for details.
Contributing

Feel free to fork, modify, or submit pull requests to enhance FloodPulse!

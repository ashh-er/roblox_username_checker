import argparse
import functools
import sys
import itertools
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import requests

# Roblox username rules:
# - 3–20 characters allowed
# - only a-z & 0-9
# - no spaces, no special characters
# - case insensitive → we generate lowercase

ALLOWED = "abcdefghijklmnopqrstuvwxyz0123456789"
MIN_LEN = 3
MAX_LEN = 5              # You can increase up to 20 later
THREADS = 5

output_lock = threading.Lock()


# ---------------------------- RULES ----------------------------
def valid_roblox(u):
    if not (MIN_LEN <= len(u) <= MAX_LEN):
        return False
    return all(c in ALLOWED for c in u)


# ---------------------- USERNAME GENERATOR ---------------------
def generate_usernames():
    for length in range(MIN_LEN, MAX_LEN + 1):
        for combo in itertools.product(ALLOWED, repeat=length):
            username = "".join(combo)
            if valid_roblox(username):
                yield username


# ---------------------- API CHECK FUNCTION ---------------------
def check_username(username):
    url = f"https://auth.roblox.com/v1/usernames/validate?username={username}&birthday=2000-01-01&context=Signup"

    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)",
            "Mozilla/5.0 (X11; Linux x86_64)"
        ])
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code == 200:
            data = r.json()
            return "Available" in data.get("message", "") or data.get("code") == 0

        elif r.status_code in (429,403):
            return "blocked"

    except:
        return "error"

    return False


# ------------------------ THREAD WORKER ------------------------
def worker(username_gen, output_file):
    while True:
        try:
            username = next(username_gen)
        except StopIteration:
            return

        result = check_username(username)

        if result:
            print(f"✔ AVAILABLE → {username}")
            with output_lock:
                output_file.write(username + "\n")
                output_file.flush()
        else:
            print(f"✖ Taken → {username}")

        if result == "blocked":
            print("\n[RATE LIMITED] Cooling 2 minutes...\n")
            time.sleep(120)

        time.sleep(random.uniform(1.2, 2.5))  # Delay helps prevent ban


# --------------------------- MAIN ------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--threads", type=int, default=THREADS)
    args = parser.parse_args()

    usernames = iter(generate_usernames())

    with open("available_roblox.txt", "a") as file:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            for _ in range(args.threads):
                executor.submit(worker, usernames, file)


if __name__ == "__main__":
    main()


    
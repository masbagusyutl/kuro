import requests
import json
import time
import random
from datetime import datetime, timedelta
import re

# Function to read authorization data from data.txt
def read_authorizations(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Function to extract username from the authorization token
def extract_username(auth_token):
    match = re.search(r'username%22%3A%22(.*?)%22', auth_token)
    if match:
        return match.group(1)
    return "Unknown"

# Function to perform pet care tasks (mining and feeding)
def perform_pet_care_tasks(auth_token, username):
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "Origin": "https://ranch.kuroro.com",
        "Pragma": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }

    mine_url = "https://ranch-api.kuroro.com/api/Clicks/MiningAndFeeding"
    for _ in range(10):  # Attempt up to 10 times
        mine_amount = random.randint(5, 10)
        feed_amount = random.randint(5, 10)
        mining_payload = json.dumps({"mineAmount": mine_amount, "feedAmount": 0})
        feeding_payload = json.dumps({"mineAmount": 0, "feedAmount": feed_amount})

        try:
            mine_response = requests.post(mine_url, headers=headers, data=mining_payload)
            feed_response = requests.post(mine_url, headers=headers, data=feeding_payload)

            if mine_response.status_code == 200 and feed_response.status_code == 200:
                print(f"[{username}] Mining with amount {mine_amount} and feeding with amount {feed_amount} successful")
            else:
                print(f"[{username}] Error in pet care tasks: {mine_response.status_code}, {feed_response.status_code}")
                break
        except Exception as e:
            print(f"[{username}] Exception in pet care tasks: {e}")
            break

# Function to claim daily diamond bonus
def claim_daily_diamond(auth_token, username):
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "Origin": "https://ranch.kuroro.com",
        "Pragma": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }

    diamond_url = "https://ranch-api.kuroro.com/api/DailyStreak/ClaimDailyBonus"

    try:
        response = requests.post(diamond_url, headers=headers)
        if response.status_code == 200:
            print(f"[{username}] Daily diamond claimed successfully")
        else:
            print(f"[{username}] Error in claiming daily diamond: {response.status_code}")
    except Exception as e:
        print(f"[{username}] Exception in claiming daily diamond: {e}")

# Function to display a countdown timer
def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f'{mins:02d}:{secs:02d}'
        print(f"Restarting in {timer}", end="\r")
        time.sleep(1)
        seconds -= 1
    print()

# Main function to process accounts
def main():
    auth_tokens = read_authorizations('data.txt')
    account_count = len(auth_tokens)
    print(f"Total accounts: {account_count}")

    next_daily_diamond_time = datetime.now()

    while True:
        for index, auth_token in enumerate(auth_tokens):
            username = extract_username(auth_token)
            print(f"Processing account {index + 1}/{account_count} ({username})")
            perform_pet_care_tasks(auth_token, username)
            if datetime.now() >= next_daily_diamond_time:
                claim_daily_diamond(auth_token, username)
                next_daily_diamond_time = datetime.now() + timedelta(days=1)
                print(f"Next daily diamond claim available on: {next_daily_diamond_time.strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(5)

        print("All accounts processed. Starting 1-hour countdown.")
        countdown_timer(3600)  # 1 hour countdown

if __name__ == "__main__":
    main()

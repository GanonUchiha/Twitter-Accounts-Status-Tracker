import tweepy
import json
import datetime
from pathlib import Path

# Create API agent
def api_setup() -> tweepy.API:
    with open("key.json") as fp:
        key: dict = json.load(fp)
    consumer_key = key["consumer_key"]
    consumer_secret = key["consumer_secret"]

    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

# Reorder the list by alphabetical order
def reorder(list_targets):
    return sorted(list(dict.fromkeys(list_targets)))

# Write search results to file
def saveResults(list_targets, list_alive, list_protected):
    # Create output folder
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    output_folder = Path("output/{}".format(date))
    output_folder.mkdir(parents=True, exist_ok=True)

    # Status (Alive/Suspended/Deleted) of all target accounts
    output_status = output_folder / "status.csv"
    print("Saving the status of the targeted accounts to {}".format(str(output_status.resolve())))
    with output_status.open("w", encoding="utf8") as fp:
        fp.write("ID,Alive,Protected\n")
        for user in list_targets:
            bool_alive     = (user in list_alive)
            bool_protected = (user in list_protected)
            fp.write(f"@{user},{bool_alive},{bool_protected}\n")
    
    # List of all target accounts
    output_accounts = output_folder / "accounts.txt"
    print("Saving a reordered list of the targeted accounts to {}".format(str(output_accounts.resolve())))
    with output_accounts.open("w") as fp:
        for user in list_targets:
            fp.write(f"https://twitter.com/{user}\n")
    
    # List of all alive accounts
    output_alive = output_folder / "alive.txt"
    print("Saving list of alive accounts to {}".format(str(output_alive.resolve())))
    with output_alive.open("w") as fp:
        fp.write("1\n")
        for idx, user in enumerate(list_alive):
            fp.write(f"https://twitter.com/{user}\n")
            if idx % 50 == 49:
                fp.write(f"\n{idx+2}\n")

def main():

    # Variables
    int_batch_size = 100            # Batch size for each api request
    api: tweepy.API = api_setup()   # Twitter API interface
    list_alive = []                 # List of accounts alive
    list_suspended = []             # List of accounts suspended
    list_protected = []             # List of accounts protected

    # Read list of target accounts
    with open("accounts.txt") as fp:
        list_targets = [x.split("/")[-1].split("(")[0].strip() for x in fp.readlines()]
        list_targets = reorder(list_targets)
    int_count = len(list_targets)
    print(f"Analysing a total number of {int_count} accounts:\n")
    
    # Lookup the status of targeted of accounts, in batches
    for int_idx_start in range(0, int_count, int_batch_size):
        int_idx_end = min(int_idx_start + int_batch_size, int_count)
        
        # print(int_idx_start, int_idx_end)
        # print(len(list_acct[int_idx_start:int_idx_end]))
        
        try:
            list_users = api.lookup_users(screen_name=list_targets[int_idx_start:int_idx_end])
        except tweepy.NotFound:
            print("No users found in batch ({}, {})".format(int_idx_start, int_idx_end))
            continue

        # print(len(list_users))

        for user in list_users:
            list_alive.append(user.screen_name)
            if user.protected:
                list_protected.append(user.screen_name)
    
    # Print out results
    print(f"Alive accounts: Total count {len(list_alive)}")
    print("@"+"\n@".join(list_alive))
    print()
    
    list_suspended = [user for user in list_targets if user not in list_alive]
    print(f"Suspended/Deleted accounts: Total count {len(list_suspended)}")
    print("@"+"\n@".join(list_suspended))
    print()
    
    print(f"Protected accounts: Total count {len(list_protected)}")
    print("@"+"\n@".join(list_protected))
    print()
    
    # Write search results to file
    saveResults(list_targets, list_alive, list_protected)
    
if __name__ == "__main__":
    main()
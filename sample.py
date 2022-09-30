import tweepy

# Basic api setup, with readonly functionality
def api_setup():
    consumer_key    = "" # Enter your api key here
    consumer_secret = "" # Enter your api secret here

    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api  = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

# Remove duplicates, and sort by ascending order
def reorganize(list_acct):
    return sorted(list(dict.fromkeys(list_acct)))

# Save the results to Respective files
def saveResults(list_acct, list_alive, list_protected):

    # accounts.txt: Save the reorganized list of accounts
    print("Saving rearranged list of accounts to accounts.txt")
    with open("accounts.txt", "w") as fp:
        for user in list_acct:
            fp.write(f"https://twitter.com/{user}\n")
    
    # status.csv: Save the status of each account
    # Possible statuses are "alive", "protected", and "suspended".
    # Note that restricted accounts are counted as "alive",
    # and suspensions might be temporary.
    print("Saving result to status.csv")
    with open("status.csv", "w", encoding="utf8") as fp:
        fp.write("ID,Alive,Protected\n")
        for user in list_acct:
            bool_alive     = (user in list_alive)
            bool_protected = (user in list_protected)
            fp.write(f"@{user},{bool_alive},{bool_protected}\n")
    
    # alive.txt: Save the list of alive accounts (not suspended),
    # in groups of 50 entries
    print("Saving list of alive accounts to alive.txt")
    with open("alive.txt", "w") as fp:
        fp.write("1\n")
        for idx, user in enumerate(list_alive):
            fp.write(f"https://twitter.com/{user}\n")
            if idx % 50 == 49:
                fp.write(f"\n{idx+2}\n")

def main():

    # Initialization
    bool_show_list = False  # Set this to True to print the account lists to standard output
    int_batch_size = 100    # Maximum number of accounts in one request, set by Twitter
    api = api_setup()
    list_alive = []
    list_suspended = []
    list_protected = []

    # Read the list of accounts in accounts.txt
    with open("accounts.txt") as fp:
        list_acct = [x.split("/")[-1].split("(")[0].strip() for x in fp.readlines()]
        list_acct = reorganize(list_acct)
    
    # Send request for the user status in batches of 100
    # The api returns an User object if the account is alive, otherwise nothing
    # See https://docs.tweepy.org/en/latest/api.html#user-methods for more info
    # For the details of User, see
    # https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user
    print(f"Analysing a total number of {len(list_acct)} accounts:\n")
    int_count = len(list_acct)
    for int_idx_start in range(0, int_count, int_batch_size):
        int_idx_end = min(int_idx_start + int_batch_size, int_count)
        list_users = api.lookup_users(screen_names=list_acct[int_idx_start:int_idx_end])
        for user in list_users:
            list_alive.append(user.screen_name)
            if user.protected:
                list_protected.append(user.screen_name)
    
    # Print the count of live accounts
    print(f"Alive accounts: Total count {len(list_alive)}")
    if bool_show_list:
        print("@"+"\n@".join(list_alive))
        print()
    
    # Print the count of suspended/deleted accounts
    list_suspended = [user for user in list_acct if user not in list_alive]
    print(f"Suspended/deleted accounts: Total count {len(list_suspended)}")
    if bool_show_list:
        print("@"+"\n@".join(list_suspended))
        print()
    
    # Print the count of protected accounts
    print(f"Protected accounts: Total count {len(list_protected)}")
    if bool_show_list:
        print("@"+"\n@".join(list_protected))
        print()
    
    # Save the results to Respective files
    saveResults(list_acct, list_alive, list_protected)
    
if __name__ == "__main__":
    main()
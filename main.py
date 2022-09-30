import tweepy

def api_setup():
    consumer_key = "EO7VkdrSr18QVKDjZqGvvE85W"
    consumer_secret = "ZW9KFx9ys23Nha26E6ibd4ZPiohvXCTntwEThaIS2fBiLBHm8G"

    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

def reorganize(list_acct):
    return sorted(list(dict.fromkeys(list_acct)))

def saveResults(list_acct, list_alive, list_protected):
    print("Saving result to status.csv")
    with open("status.csv", "w", encoding="utf8") as fp:
        fp.write("ID,Alive,Protected\n")
        for user in list_acct:
            bool_alive     = (user in list_alive)
            bool_protected = (user in list_protected)
            fp.write(f"@{user},{bool_alive},{bool_protected}\n")
    
    print("Saving rearranged list of accounts to accounts.txt")
    with open("accounts.txt", "w") as fp:
        for user in list_acct:
            fp.write(f"https://twitter.com/{user}\n")
    
    print("Saving list of alive accounts to accounts.txt")
    with open("alive.txt", "w") as fp:
        fp.write("1\n")
        for idx, user in enumerate(list_alive):
            fp.write(f"https://twitter.com/{user}\n")
            if idx % 50 == 49:
                fp.write(f"\n{idx+2}\n")

def main():
    int_batch_size = 100
    api = api_setup()
    list_alive = []
    list_suspended = []
    list_protected = []

    with open("accounts.txt") as fp:
        list_acct = [x.split("/")[-1].split("(")[0].strip() for x in fp.readlines()]
        list_acct = reorganize(list_acct)
    print(f"Analysing a total number of {len(list_acct)} accounts:\n")
    int_count = len(list_acct)
    for int_idx_start in range(0, int_count, int_batch_size):
        int_idx_end = min(int_idx_start + int_batch_size, int_count)
        ## print(int_idx_start, int_idx_end)
        ## print(len(list_acct[int_idx_start:int_idx_end]))
        list_users = api.lookup_users(screen_names=list_acct[int_idx_start:int_idx_end])
        ## print(len(list_users))
        for user in list_users:
            list_alive.append(user.screen_name)
            if user.protected:
                list_protected.append(user.screen_name)
    
    print("Alive accounts:")
    print("@"+"\n@".join(list_alive))
    print()
    
    list_suspended = [user for user in list_acct if user not in list_alive]
    print(f"Suspended/Non-existing accounts: Total count {len(list_suspended)}")
    print("@"+"\n@".join(list_suspended))
    print()
    
    print(f"Protected accounts: Total count {len(list_protected)}")
    print("@"+"\n@".join(list_protected))
    print()
    
    saveResults(list_acct, list_alive, list_protected)
    
if __name__ == "__main__":
    main()
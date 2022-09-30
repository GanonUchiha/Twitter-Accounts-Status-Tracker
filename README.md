# Twitter Accounts Tracker

A simple Python program that tracks the statuses of a list of twitter accounts.

## Objective
Given a list of twitter accounts, look up their current status (alive, suspended/deleted, protected).

## Usage
1. Create a file `key.json`, including credentials of your Twitter API App. For example:
    ```json
    {
        "consumer_key": "Your consumer key",
        "consumer_secret": "Your consumer secret"
    }
    ```
    Do not share this information to anyone.
1. Create a file `accounts.txt`, including a list of accounts (URL or username). For example:
    ```
    @YouTube
    @Twitter
    https://twitter.com/NASA
    https://twitter.com/discord
    ```
1. run `python src/main.py` in your command prompt, and the results should show up in the `output` folder.

## Environment

This program uses the following packages:
- python 3.10.4
- tweepy 4.10.1

Detailed packages and versions can be found in `requirements.txt`. To create an identical virtual environment in Anaconda, use the command `conda create --name <env> --file requirements.txt`.
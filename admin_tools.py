import os
import tweepy
from dotenv import load_dotenv
import db_connector

load_dotenv()

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")


def update_all_posted():
    db_connector.update_all_posted()
    print("All records updated to posted.")


def delete_all_tweets():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    for status in tweepy.Cursor(api.user_timeline).items():
        try:
            api.destroy_status(status.id)
        except Exception as err:
            pass
    print("All tweets deleted.")


def main_menu():
    print("=====================================")
    print("Welcome to admin tools")
    print("1. Delete all tweets")
    print("2. Update all records to posted")
    print("3. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        confirm = input("Are you sure you want to delete all tweets? type 'yes' to confirm: ")
        if confirm == 'yes':
            delete_all_tweets()
        else:
            print("Deletion cancelled.")
            main_menu()
    elif choice == '2':
        update_all_posted()
    elif choice == '3':
        exit()
    else:
        print("Invalid choice, please try again.")
    main_menu()


if __name__ == "__main__":
    main_menu()

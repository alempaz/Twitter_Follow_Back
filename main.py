import tweepy
from time import sleep
# APP Permission needs to be Read/Write

# Keys
# region
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
bearer_token = ''
# endregion
# Auth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# https://docs.tweepy.org/en/v3.5.0/api.html - wrapper references
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
user_me = api.me()
friends = api.friends_ids(api.me().id)


# Request windows are 15 minutes in length
# https://developer.twitter.com/ja/docs/basics/rate-limits
# Function to work around Twitter's Rate Limit
def limit_handler(cursor):
    try:
        while True:
            yield cursor.next()
    except tweepy.RateLimitError:
        # Seconds
        sleep(5)


# Get list of users followed
def user_followed(count, user_list):
    print(f'Done. You followed {count} new users.')
    print('Usernames followed:')
    for i in user_list:
        print(i)


# ------------------------- Follow Back Bot -------------------------
# Following a specific username
def follow_specific_username(username):
    print(f'Searching for a follower called @{username} and following back...')

    for follower in limit_handler(tweepy.Cursor(api.followers).items()):
        if follower.screen_name == username:
            if follower.id in friends:
                print(f'You already followed @{follower.screen_name}.')
                break
            else:
                follower.follow()
                print(f'@{follower.name} was followed!')
                break
    print(f'@{username} was not found in your followers.')


# following users that have more than 10,000k followers
def follow_popular_followers():
    followed_back_users = []
    count = 0
    print('Getting followers that have more than 10,000k Followers, and following them back...\n')

    for follower in limit_handler(tweepy.Cursor(api.followers).items()):
        if follower.followers_count >= 10000:
            if follower.id in friends:
                print(f'You already followed @{follower.screen_name}.')
            else:
                follower.follow()
                followed_back_users.append(follower.screen_name)
                count += 1
                print(f'{follower.name} was followed! Followers Count: {follower.followers_count}')
    user_followed(count, followed_back_users)


# Follow everybody!
def follow_back_everyone():
    followed_back_users = []
    count = 0
    print('Getting followers and following them back...')

    for follower in limit_handler(tweepy.Cursor(api.followers).items()):
        if follower.id != api.me().id:
            if follower.id in friends:
                print(f'You already followed @{follower.screen_name}.')
            else:
                follower.follow()
                followed_back_users.append(follower.screen_name)
                count += 1
                print(f'Started Following @{follower.screen_name}!')
    user_followed(count, followed_back_users)

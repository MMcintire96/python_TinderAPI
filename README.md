# Tinder api -> Python-bindings

This project contains python bindings for the unoffical tinder api. The tinder api is constantly changing and current libraries are not always up to date. This project is a mix of Pynder's style and Fbessez's endpoints/auth. Work is currently in progress, but suitable for non-production projects.

## Getting Started

You will need to insert your tinder_token in the utils/config.py file. This currently uses SMS auth method for verification as FaceBook auth has changed.

To get your tinder_token run sms_auth.py and enter your phone number registered to your tinder account and the code they send you.

Clone this repo, in your project import tinder_api and get to work. The example.py shows how to get rolling.

## Usage

```
import tinder_api.session

sess = tinder_api.session.Session() # creates a session

print(sess.meta) # prints your meta data
sess.update_profile(bio="I love VIM") # updates your bio - see kwargs

for user in sess.yield_users():
    user.name
    user.id
    user.age
    user.bio
    user.gender # male or female
    user.photos # url of the photos
    user.like() # swipe right
    user.pass() # swipe left
    user.super_like() # swipe up

    user.report(1) # report for spam

for match in sess.yield_matches():
    match.name # all the same endpoints as a normal user
    match.match_data # contains match data like messages/profile
    match.message('Hello, I use VIM so I am superior to all those other programmers you've dated')
    match.get_messages()
```

## Authors/Acknowledgments
* ** Michael ** - *Initial Work* [MMcintire96](https://github.com/MMcintire96)
* ** Sharkbound ** - *Json Wrapper* [sharkbound](https://github.com/sharkbound)
* ** Wowotek ** - *Pull requests, cleanup and design* [wowotek](https://github.com/wowotek)


## TODO

1. Move more methods to JsonWrapper
2. Optimize for speed -- UserController + NormalUser = 1.5s, MatchUser = 3.0s
3. Maybe add Routes.py
4. Fix FB Auth Method

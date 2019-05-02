import tinder_api
import json

sess = tinder_api.sess.Profile()

for user in sess.yield_usersv2():
    print(user.name)




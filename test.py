import tinder_api.session
import json

sess = tinder_api.session.Session()

for user in sess.yield_users():
    print(user.name)





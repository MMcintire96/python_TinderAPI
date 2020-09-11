import tinder_api.session

sess = tinder_api.session.Session() # creates a session

print(sess.meta) # prints your meta data
# sess.update_profile(bio="I love VIM") # updates your bio - see kwargs

for user in sess.yield_users():
    print(user.name)
    print(user.id)
    print(user.age)
    print(user.bio)
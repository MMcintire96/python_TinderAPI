import tinder_api.session
import itertools

sess = tinder_api.session.Session() # inits the session

print("My _id is %s" %sess.get_id())

#sess.update_profile(bio="VIM is the best")

for user in itertools.islice(sess.yield_users(), 3):
    print(user.name) # prints the name of the user see __init__
    print(user.like()) # returns false if not a match

for match in sess.yield_matches():
    print(match.name)
    print(match.match_data) # prints all the match_data
    print([x.body for x in match.get_messages()]) # gets the body of messages
    #print(match.message("Hello")) # sends hello to the match



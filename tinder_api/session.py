from utils.request_handlers import post
import utils.config as c

class Session():
    def auth():
        req = r.post('/auth/login/accountkit', {'token': c.tinder_token})
        return req

print(Session.auth())

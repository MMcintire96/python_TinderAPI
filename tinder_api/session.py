import requests

from tinder_api.utils import request_handlers as r
from tinder_api.utils import config as c
from tinder_api import user as u

class Session():
    def __init__(self):
        self.auth = self.auth()
        self.id = self.get_id()
        #self.me = self.me()
        self.data = r.get('/profile')
        self.meta = r.get('/meta')
        self.metav2 = r.get('/v2/meta')

    def auth(self):
        req = r.post('/auth/login/accountkit', {'token': c.tinder_token, 'id': c.tinder_token, 'client_version': '9.0.1'})
        return req

    def get_id(self):
        return r.get('/profile')['_id']

    def me(self):
        return u.UserController(r.get('/profile')['_id']).get_user()

    def yield_users(self):
        while True:
            resp = r.get('/user/recs')
            recs = resp['results'] if 'results' in resp else []
            for rec in recs:
                yield u.UserController(rec['_id']).get_user()

    def yield_usersv2(self):
        while True:
            resp = r.get('/v2/recs/core?locale=en-US')
            recs = resp['data']['results'] if 'data' in resp else []
            for rec in recs:
                if rec['type'] == 'user':
                    yield u.UserController(rec['user']['_id']).get_user()

    #fix this _id = match_id rn
    def yield_matches(self):
        resp = r.post('/updates', {"last_activity_date": ""})
        for match in reversed(resp['matches']):
            yield u.UserController(match['_id']).get_user()

    def list_matches(self):
        return r.post('/updates', {"last_activity_date": ""})['matches']

    def get_updates(self, data=''):
        return r.post('/updates', {"last_activity_date": date})

    def update_profile(self, **kwargs):
        try:
            return r.post('/profile', kwargs)
        except Exception as e:
            print('Error in updating profile: ', e)

    def change_location(self, lat, lon):
        resp = r.post('/passport/user/travel', {"lat": lat, "lon": lon})
        if 'error' in resp:
            return "Could not change location. Remeber +-=NS_lat and +-=EW_lon"
        return resp

    def reset_location(self):
        resp = r.post('/passport/user/reset', {})
        if 'error' in resp:
            return "Could not change location. Are you a tinder+ user?"
        return resp

    def change_username(self, uname):
        if len(uname) > 20:
            return "Username max length = 20"
        resp = r.put(url, {"username": uname})
        if 'error' in resp.json():
            return resp.json()['error']
        else:
            return 'Username Updated'

    def reset_username(self):
        return r.delete('/profile/username', headers=config.headers)

    def trending_gifs(self, limit=3):
        return r.get('/giphy/trending?limit={}'.format(limit))

    def search_gifs(self, query, limit=3):
        return r.get('/giphy/search?limit={}&query={}'.format(limit, query))

    def fast_match_count(self):
        return r.get('/v2/fast-match/count')['data']['count']

    #.content doesnt work with the current get handler
    def fast_match_img(self):
        return requests.get('/v2/fast-match/preview' , headers=config.headers).content

if __name__ == '__main__':
    pass

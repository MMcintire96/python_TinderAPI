import requests

from tinder_api import user as u
from tinder_api.utils import config as c
from tinder_api.utils import request_handlers as r


class Session():
    def __init__(self):
        self.id = self.get_id()
        self.data = r.get('/profile')
        self.meta = r.get('/meta')
        self.metav2 = r.get('/v2/meta')


    def get_id(self):
        """Returns the _id of the Session"""
        return r.get('/profile')['_id']

    def me(self):
        """Returns a UserModel() for the Session"""
        return u.UserController(r.get('/profile')['_id']).get_user()

    def yield_users(self):
        """Returns a generator of nearby users as NormalUser()"""
        while True:
            resp = r.get('/user/recs')
            recs = resp['results'] if 'results' in resp else []
            for rec in recs:
                yield u.UserController(rec['_id']).get_user()

    def yield_usersv2(self):
        """Returns a generator of nearby users as NormalUser() and calculates location"""
        while True:
            resp = r.get('/v2/recs/core?locale=en-US')
            recs = resp['data']['results'] if 'data' in resp else []
            for rec in recs:
                if rec['type'] == 'user':
                    yield u.UserController(rec['user']['_id']).get_user()

    def yield_matches(self):
        """Returns a generator of matches as MatchUsers()"""
        resp = r.post('/updates', {"last_activity_date": ""})
        for match in reversed(resp['matches']):
            yield u.UserController(match['_id']).get_user()

    def list_matches(self):
        """Returns a [] of matches"""
        return r.post('/updates', {"last_activity_date": ""})['matches']

    def get_updates(self, date=''):
        """Returns the profile 'updates' since date
        Date formatting is specific:
            date = '2017-03-25T20:58:00.404z"
            if date='' then returns updates since profile was made
        """
        return r.post('/updates', {"last_activity_date": date})

    def update_profile(self, **kwargs):
        """Updates the session profile
        Kwargs - not all are known, type specific (int, str, dict, bool):
            age_filter_min=20
            age_filter_max=30
            bio='new bio who dis'
            distance_filter=100
            discoverable=true
            gender=1 <- seeking females
            {"photo_optimizer_enabled":false}
        """
        try:
            return r.post('/profile', kwargs)
        except Exception as e:
            print('Error in updating profile: ', e)

    def change_location(self, lat, lon):
        """Changes the session user's location for Tinder+"""
        resp = r.post('/passport/user/travel', {"lat": lat, "lon": lon})
        if 'error' in resp:
            return "Could not change location. Remeber +-=NS_lat and +-=EW_lon"
        return resp

    def reset_location(self):
        """Resets the session user's location to original location for Tinder+"""
        resp = r.post('/passport/user/reset', {})
        if 'error' in resp:
            return "Could not change location. Are you a tinder+ user?"
        return resp

    def change_username(self, uname):
        """Changes the session user's username. Not the same as Name"""
        if len(uname) > 20:
            return "Username max length = 20"
        resp = r.put(url, {"username": uname})
        if 'error' in resp.json():
            return resp.json()['error']
        else:
            return 'Username Updated'

    def reset_username(self):
        """Resets the session user's username"""
        return r.delete('/profile/username', headers=config.headers)

    def trending_gifs(self, limit=3):
        """Returns the trending gifs based on limit=int(amount)"""
        return r.get('/giphy/trending?limit={}'.format(limit))

    def search_gifs(self, query, limit=3):
        """Returns the limit=int(amount) of gifs based on the query -> see giphy docs"""
        return r.get('/giphy/search?limit={}&query={}'.format(limit, query))

    def fast_match_count(self):
        """Returns the number of like's the session user has received"""
        return r.get('/v2/fast-match/count')['data']['count']

    def fast_match_img(self):
        """Returns the blurred image thumbnails of users in fast-match, TinderGold"""
        return requests.get('/v2/fast-match/preview' , headers=config.headers).content

if __name__ == '__main__':
    pass

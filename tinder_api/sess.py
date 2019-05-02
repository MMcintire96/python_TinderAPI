import json

import requests

from tinder_api import config
from tinder_api import user_model

#test wrapper from sharkbound
#from tinder_api.utils import wrapper

class Profile(object):

    def __init__(self):
        self.api_base = config.host
        self.data = self.get('/profile')
        #self.test = wrapper.json_to_object(self.get('/profile'))
        self.meta = self.get('/meta')
        self.metav2 = self.get('/v2/meta')
        self.id = self.data['_id']
        self.name = self.data['name']
        self.bio = self.data['bio']
        self.gender = self.decode_gender(self.data['gender'])
        self.interested_in = self.decode_gender(self.data['interested_in'][0])
        self.city = self.data['pos_info']['city']['name']
        self.state = self.data['pos_info']['state']['name']
        self.country = self.data['pos_info']['country']['name']
        self.location = self.city + ', ' + self.state + ', ' + self.country
        self.ping_time = self.data['ping_time']
        self.school_name = [x['name'] for x in self.data['schools']]
        self.school_id = [x['id'] for x in self.data['schools']]
        self.jobs = [x for x in self.data['jobs']]
        self.photos = [x['url'] for x in self.data['photos']]

    def get(self, url):
        full_url = self.api_base + url
        r = requests.get(full_url, headers=config.headers)
        return r.json()

    def post(self, url, p_data):
        full_url = self.api_base + url
        r = requests.post(full_url, headers=config.headers,
                data=json.dumps(p_data))
        return r.json()

    def decode_gender(self, gender):
        if gender == 0:
            return "male"
        elif gender == 1:
            return "female"

    def yield_usersv2(self):
        while True:
            r = self.get('/v2/recs/core?locale=en-US')
            recs = r['data']['results'] if 'data' in r else []
            for rec in recs:
                if rec['type'] == 'user':
                    yield user_model.UserModel(rec['user']['_id'])

    def yield_users(self):
        while True:
            r = self.get('/user/recs')
            recs = r['results'] if 'results' in r else []
            for rec in recs:
                yield user_model.UserModel(rec['_id'])

    def yield_matches(self):
        r = self.post('/updates', {"last_activity_date": ""})
        for match in reversed(r['matches']):
            yield user_model.UserModel(match['_id'])

    def list_matches(self):
        r = self.post('/updates', {"last_activity_date": ""})
        return r['matches']

    # format is "2017-07-09T10:30:13.432Z"
    def updates(self, date=''):
        return self.post('/updates', {'last_activity_date': date})

    #test all kwargs
    def update_profile(self, **kwargs):
        try:
            return self.post('/profile', kwargs)
        except Exception as e:
            print('Error in updating profile: ', e)

    def change_location(self, lat, lon):
        r = self.post('/passport/user/travel', {"lat": lat, "lon": lon})
        if 'error' in r:
            return "Could not change location. Remeber +-=NS_lat and +-=EW_lon"
        return r

    def reset_location(self):
        r = self.post('/passport/user/reset', {})
        if 'error' in r:
            return "Could not change location. Are you a tinder+ user?"
        return r

    def change_username(self, uname):
        if len(uname) > 20:
            return "Username max length = 20"
        url = self.api_base + '/profile/username'
        r = requests.put(url, headers=config.headers,
                data=json.dumps({"username": uname}))
        resp = r.json()
        if 'error' in resp:
            return resp['error']
        else:
            return 'Username Updated'

    def reset_username(self):
        url = self.api_base + '/profile/username'
        return requests.delete(url, headers=config.headers)

    def trending_gifs(self, limit=3):
        return self.get('/giphy/trending?limit={}'.format(limit))

    def search_gifs(self, query, limit=3):
        return self.get('/giphy/search?limit={}&query={}'.format(limit, query))

    def fast_match_count(self):
        return self.get('/v2/fast-match/count')['data']['count']

    def fast_match_img(self):
        url = self.api_base + '/v2/fast-match/preview'
        return requests.get(url, headers=config.headers).content


if __name__ == '__main__':
    pass

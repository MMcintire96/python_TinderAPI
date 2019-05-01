import datetime
import json
import re

import dateutil.parser
import requests
from bs4 import BeautifulSoup

import sess
import config


class UserModel(object):
    def __init__(self, u_id):
        self.sess = sess.Profile()
        self.id = self.reshape_id(u_id)
        self.data = self.get_data()
        self.match_data = self.get_match_data(u_id)

    def get_data(self):
        r = self.sess.get('/user/{}'.format(self.id))
        return r['results']

    def like(self):
        r = self.sess.get('/like/{}'.format(self.id))
        return r['match']

    def super_like(self):
        r = self.sess.post('/like/{}/super'.format(self.id), {})
        return r['match']

    def dislike(self):
        r = self.sess.get('/pass/{}'.format(self.id))
        return 'passed'

    def report(self, cause, text=''):
        r = self.sess.post('/report/{}'.format(self.id),
                {"cause": cause, "text": text})
        return r

    def get_match_data(self, u_id):
        for match in self.sess.list_matches():
            if match['participants'][0] == u_id:
                self.match_id = match['_id']
                self.is_match = True
                return match
            else:
                self.match_id = None
                self.is_match = False
                self.match_data = None

    def reshape_id(self, u_id):
        if self.sess.id in u_id:
            return u_id.replace(self.sess.id, '')
        else:
            return u_id

    def message(self, body):
        if self.is_match == True and self.match_id is not None:
            full_url = config.host + '/user/matches/{}'.format(self.match_id)
            d = {"message": str(body)}
            r = requests.post(full_url, headers=config.headers,
                            data=json.dumps(d))
            return r.json()['sent_date']
        else:
            raise Exception('User is not a match')

    @property
    def messages(self):
        if self.is_match == True:
            return [x['message'] for x in self.match_data['messages']]
        else:
            raise Exception('User is not a match')

    @property
    def bio(self):
        return self.data['bio'] if 'bio' in self.data else None

    @property
    def name(self):
        return self.data['name']

    @property
    def birth_date(self):
        return dateutil.parser.parse(self.data['birth_date'])

    @property
    def age(self):
        today = datetime.date.today()
        return (today.year - self.birth_date.year -
                ((today.month, today.day) <
                (self.birth_date.month, self.birth_date.day)))

    @property
    def gender(self):
        if self.data['gender'] == 0:
            return 'male'
        elif self.data['gender'] == 1:
            return 'female'

    @property
    def distance_mi(self):
        if 'distance_mi' in self.data:
            return int(self.data['distance_mi'])
        return None

    @property
    def distance_km(self):
        if 'distance_km' in self.data:
            return self.data['distance_km']
        return int(self.distance_mi * 1.6093)

    @property
    def jobs(self):
        if 'jobs' in self.data and len(self.data['jobs']) > 0:
            try:
                job_loco = self.data['jobs'][0]['company']['name']
                job_title = self.data['jobs'][0]['title']['name']
                return [job_title + ' @ ' + job_loco]
            except Exception as e:
                return None
        return None

    @property
    def school_name(self):
        if 'schools' in self.data:
            try:
                return self.data['schools'][0]['name']
            except Exception as e:
                return None
        return None

    @property
    def school_id(self):
        if 'schools' in self.data:
            try:
                return self.data['schools'][0]['id']
            except Exception as e:
                return None
        return None

    @property
    def schools(self):
        # get this working?
        return school_dict

    @property
    def ping_time(self):
        return self.data['ping_time']

    @property
    def photos(self):
        return [x['url'] for x in self.data['photos']]

    @property
    def instagram_username(self):
        if 'instagram' in self.data:
            x = requests.get(self.data['instagram']['photos'][0]['link'])
            soup = BeautifulSoup(x.text, 'html5lib')
            meta_str = soup.find('meta',
                    attrs={'property': 'og:description'})['content']
            ig_uname = re.findall('@[^\s|\W]*', meta_str)
            return ig_uname[0][1:]
        return None

    @property
    def spotify(self):
        if 'spotify_top_artists' in self.data:
            return [{'name': s['top_track']['name'],
                    'id': s['top_track']['id'],
                    'artist': s['top_track']['artists'][0]['name']}
                    for s in self.data['spotify_top_artists']]
        return None

    @property
    def spotify_theme(self):
        if 'spotify_theme_track' in self.data:
            return [{'name': self.data['spotify_theme_track']['name'],
                    'id': self.data['spotify_theme_track']['id'],
                    'artist': self.data['spotify_theme_track']['artists'][0]['name']}]
        return None

    @property
    def instagram_photos(self):
        if 'instagram' in self.data:
            return [x['image'] for x in self.data['instagram']['photos']]
        return None


if __name__ == '__main__':
    pass

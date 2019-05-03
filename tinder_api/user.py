from tinder_api import session
from tinder_api.utils import request_handlers as r
from tinder_api.utils.wrapper import JsonWrapper

import json
import datetime
import dateutil.parser

class UserModel():
    def __init__(self, uid, name, bio, age, birth_date, photos,
            gender, distance, job_name, job_title, school_name,
            school_id, ping_time, top_song, instagram_photos):
        self.id = uid
        self.name = name
        self.bio = bio
        self.age = age
        self.birth_date = birth_date
        self.photos = photos
        self.gender = gender
        self.distance = distance
        self.job_name = job_name
        self.job_title = job_title
        self.school_name = school_name
        self.school_id = school_id
        self.ping_time = ping_time
        self.top_song = top_song
        self.instagram_photos = instagram_photos

    def report(self, cause, text=''):
        """Reports the user
        Cause:
            0 : 'other' requires text
            1 : 'spam'
            4 : 'inappropriate photos'
        """
        resp = r.post('/report/{}'.format(uid),
                {"cause": cause, "text": text})
        return resp

class NormalUser(UserModel):
    def __init__(self, uid, name, bio, age, birth_date, photos, gender,
                distance, job_name, job_title, school_name, school_id,
                ping_time, top_song, instagram_photos):
        super().__init__(uid, name, bio, age, birth_date, photos, gender,
                distance, job_name, job_title, school_name, school_id,
                ping_time, top_song, instagram_photos)

    def like(self):
        """Likes (swipes right) the user"""
        resp = r.get('/like/{}'.format(self.id))
        return resp['match']

    def super_like(self):
        """Super likes (swipes up) the user"""
        resp = r.post('/like/{}/super'.format(self.id), {})
        return resp['match']

    def dislike(self):
        """Dislikes (swipes left) the user"""
        resp = r.post('/pass/{}'.format(self.id))
        return 'passed'


class MatchUser(UserModel):
    def __init__(self, uid, match_id, name, bio, age, birth_date, photos, gender,
                distance, job_name, job_title, school_name, school_id,
                ping_time, top_song, instagram_photos):
        super().__init__(uid, name, bio, age, birth_date, photos, gender,
                distance, job_name, job_title, school_name, school_id,
                ping_time, top_song, instagram_photos)

        self.match_id = match_id
        self.match_data = self.get_match_data()

    def get_match_data(self):
        """Returns a [] of match data"""
        return [x for x in session.Session().list_matches() if x['_id'] == self.match_id][0]

    def message(self, body):
        """Messages the user"""
        resp = r.post('/user/matches/{}'.format(self.match_id),
                {"message": str(body)})
        return resp['sent_date']

    def get_messages(self):
        """Constructs a Message() object for each message"""
        return [Message(x, self.id, self.name) for x in self.match_data['messages']]

class Message():
    def __init__(self, data, uid, name):
        self.message_id = data['_id']
        self.data = data
        self.sent = dateutil.parser.parse(data['sent_date'])
        self.body = data['message']
        if data['from'] == uid:
            self.sender = name
        else:
            self.sender = "Me"
        if data['to'] == uid:
            self.to = name
        else:
            self.to = "Me"

    def like_message(self):
        """Likes a message"""
        resp = r.post('/message/{}/like'.format(self.message_id), {})
        if 'error' in resp:
            return "Error, unable to like message"
        return resp

    def unlike_message(self):
        """Unlikes a message"""
        resp = r.delete('/message/{}/like'.format(self.message_id))
        if resp.status_code == 204:
            return resp
        return "Error, unable to unlike the message"

    def is_liked(self):
        """Returns True if the messages is liked, otherwise False"""
        liked_messages = [x['message_id'] for x in session.Session().get_updates()['liked_messages']]
        for mess_id  in liked_messages:
            if mess_id == self.message_id:
                return True
        return False

    def __unicode__(self):
        return self.body

    def __str__(self):
        return self.body.encode('utf-8')

    def __repr__(self):
        return repr(self.body)



class UserController:
    def __init__(self, uid):
        self.id = uid
        self.me_id = session.Session().get_id()
        self.user_type = self._decode_user_type()
        self.data = self.get_data()
        self.const = JsonWrapper(self.data, iter_keys_only=False)

    def get_data(self):
        """Returns the data of the user"""
        if self.user_type is 'Me':
            data = r.get('/profile')
            return data
        else:
            data = r.get('/user/{}'.format(self.id))
        if 'error' in data:
            print('Error user was not found')
        return data['results']

    def _decode_user_type(self):
        """Returns the user_type (Me, Match, Normal) based on uid"""
        if self.me_id == self.id:
            return 'Me'
        elif self.me_id in self.id:
            self.match_id = self.id
            self.id = self.id.replace(self.me_id, '')
            return 'Match'
        else:
            return 'Normal'

    def get_user(self):
        """Constructs the correct User Object based on user_type"""
        name = self.const.name
        bio = self.const.bio
        birth_date = self._decode_birth_date()
        age = self._decode_age()
        photos = [photo.url for photo in self.const.photos]
        gender = self._decode_gender()
        distance = self._decode_distance()
        job_name = self.const.jobs[0].company.name
        job_title =  self.const.jobs[0].title.name
        school_name = self.const.schools[0].name
        school_id = self.const.schools[0].id
        ping_time = self.const.ping_time
        top_song = self._decode_theme_song()
        instagram_photos = [photo.image for photo in self.const.instagram.photos]
        if self.user_type is 'Normal':
            return NormalUser(self.id, name, bio, age, birth_date, photos, gender,
                    distance, job_name, job_title, school_name, school_id,
                    ping_time, top_song, instagram_photos)
        elif self.user_type is 'Match':
            return MatchUser(self.id, self.match_id, name, bio, age, birth_date, photos, gender,
                    distance, job_name, job_title, school_name, school_id,
                    ping_time, top_song, instagram_photos)
        elif self.user_type is 'Me':
            return UserModel(self.id, name, bio, age, birth_date, photos, gender,
                    distance, job_name, job_title, school_name, school_id,
                    ping_time, top_song, instagram_photos)

    def _decode_birth_date(self):
        """Returns the human readable birth_date"""
        return dateutil.parser.parse(self.const.birth_date)

    def _decode_age(self):
        """Returns age as an int"""
        today = datetime.date.today()
        return (today.year - self._decode_birth_date().year -
                ((today.month, today.day) <
                (self._decode_birth_date().month,
                self._decode_birth_date().day)))

    def _decode_gender(self):
        """Converts gender to a human readable format"""
        gender = self.const.gender
        if gender is 1:
            return 'female'
        elif gender is 0:
            return 'male'

    def _decode_distance(self):
        """Returns distance in miles"""
        if 'distance_mi' in self.data:
            return self.const.distance_mi
        elif 'distance_km' in self.data:
            return self.const.distance_km * 0.621371

    def _decode_jobs(self):
        """Returns a [] of job names"""
        return [job.company.name for job in self.const.jobs]

    def _decode_theme_song(self):
        """Returns a {name, id, artist} of the user's spotify theme"""
        theme_s = self.const.spotify_theme_track
        return {'name': theme_s.name,
                'id': theme_s.id,
                'artist': theme_s.artists[0].name}

if __name__ == '__main__':
    pass

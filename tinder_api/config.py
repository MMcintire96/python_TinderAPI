import json

import requests

from tinder_api.utils import fb_auth

fb_email = "fb_name"
fb_password = "fb_pass"
#fb_auth_token = fb_auth.get_fb_access_token(fb_email, fb_password)
#fb_user_id = fb_auth.get_fb_id(fb_auth_token)

tinder_token = "33660983-b36a-4882-b081-cad76ae4b03d"

headers = {
    'app_version': '6.9.4',
    'platform': 'ios',
    'content-type': 'application/json',
    'User-agent': 'Tinder/7.5.3 (iPohone; iOS 10.3.2; Scale/2.00)',
    'X-Auth-Token': tinder_token,
}

host = 'https://api.gotinder.com'

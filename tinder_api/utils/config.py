#from tinder_api.utils import fb_auth


# Depreciated from facebook v2 changes
#fb_email = "fb_name"
#fb_password = "fb_pass"
#fb_auth_token = fb_auth.get_fb_access_token(fb_email, fb_password)
#fb_user_id = fb_auth.get_fb_id(fb_auth_token)

tinder_token = "b90943fd-39a1-404d-bfa0-2a4731c36105"
host = 'https://api.gotinder.com'
headers = {
    'app_version': '6.9.4',
    'platform': 'ios',
    'content-type': 'application/json',
    'User-agent': 'Tinder/7.5.3 (iPohone; iOS 10.3.2; Scale/2.00)',
    'X-Auth-Token': tinder_token,
}


if __name__ == '__main__':
    pass

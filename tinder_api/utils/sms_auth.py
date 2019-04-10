#cite source for this code
#github fbessez

import json

import requests

REQ_URL = "https://graph.accountkit.com/v1.2/start_login?access_token=AA%7C464891386855067%7Cd1891abb4b0bcdfa0580d9b839f4a522&credentials_type=phone_number&fb_app_events_enabled=1&fields=privacy_policy%2Cterms_of_service&locale=fr_FR&phone_number=#placeholder&response_type=token&sdk=ios"
VALIDATE_URL = "https://graph.accountkit.com/v1.2/confirm_login?access_token=AA%7C464891386855067%7Cd1891abb4b0bcdfa0580d9b839f4a522&confirmation_code=#confirmation_code&credentials_type=phone_number&fb_app_events_enabled=1&fields=privacy_policy%2Cterms_of_service&locale=fr_FR&login_request_code=#request_code&phone_number=#phone_number&response_type=token&sdk=ios"
TOKEN_URL = "https://api.gotinder.com/v2/auth/login/accountkit"

HEADERS = { 'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Mobile/15D60 AKiOSSDK/4.29.0'}

def send(num):
    URL = REQ_URL.replace("#placeholder", str(num))
    r = requests.post(URL, headers=HEADERS, verify=False)
    response = r.json()
    if (response.get("login_request_code") == None):
        return False
    else:
        print("sending code")
        return response["login_request_code"]

def getToken(num, code, req_code):
    VAL_URL = VALIDATE_URL.replace("#confirmation_code", code)
    VAL_URL = VAL_URL.replace("#phone_number", num)
    VAL_URL = VAL_URL.replace("#request_code", req_code)
    r_validate = requests.post(VAL_URL, headers=HEADERS, verify=False)
    validate_response = r_validate.json()
    access_token = validate_response["access_token"]
    access_id = validate_response["id"]
    GetToken_content = json.dumps({'token': access_token, 'id': access_id, 'client_version': '9.0.1'})
    GetToken_headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Mobile/15D60 AKiOSSDK/4.29.0', 'Content-Type':'application/json'}
    r_GetToken = requests.post(TOKEN_URL, data=GetToken_content, headers=GetToken_headers, verify=False)
    token_response = r_GetToken.json()
    if (token_response["data"].get("api_token") == None):
        return token_response
    else:
        return token_response["data"]["api_token"]


def get_sms_token(num):
    log_code = send(num)
    sms_code = input("Enter Code ")
    return getToken(num, sms_code, log_code)

print(get_sms_token(input('enter phone in format of 1+phone_num: ')))

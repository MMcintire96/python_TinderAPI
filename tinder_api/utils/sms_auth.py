import requests
import json

base_url = "https://api.gotinder.com/v2/auth/"
headers = {
        "User-Agent" : "Tinder/11.4.0 (iPhone; iOS 12.4.1; Scale/2.00)",
        "Content-Type" : "application/json"
}

def send_number():
    phone_number = str(input("Enter your phone number in form 3211234567: "))
    phone_number = "1+"+phone_number
    url = base_url+"sms/send?auth_type=sms"
    data = {"phone_number": phone_number}
    resp = requests.request("POST", url,
            data=json.dumps(data), headers=headers)
    return phone_number

def validate_code(phone_number):
    url = base_url+"sms/validate?auth_type=sms"
    otp_code = input(f"Enter the tinder code sent to {phone_number}: ")
    data = {
            "otp_code": otp_code,
            "phone_number": phone_number
    }
    resp = requests.request("POST", url,
            data=json.dumps(data), headers=headers)
    return resp.json()['data']['refresh_token']

def save_token():
    phone_number = send_number()
    refresh_token = validate_code(phone_number)
    url = base_url+"/login/sms"
    data = {"client_version" : "11.4.0", "refresh_token": refresh_token}
    resp = requests.request("POST", url,
            data=json.dumps(data), headers=headers)
    api_token = resp.json()['data']['api_token']
    with open('token.txt', 'w') as f:
        f.write(api_token)
    print(api_token)

if __name__ == "__main__":
    save_token()

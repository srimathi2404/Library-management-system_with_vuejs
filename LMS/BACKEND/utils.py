import requests
import json

def send_message(webhook_url, message):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }

    payload = {
        'text': message
    }

    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("Message sent successfully")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending message : {str(e)}")
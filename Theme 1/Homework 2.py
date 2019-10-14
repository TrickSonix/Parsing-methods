import requests
import json
import time
from settings import ACCESS_TOKEN

#получим список друзей пользователя с помощью API вконтакте


def get_list_of_friends(access_token):
    url = 'https://api.vk.com/method/friends.get?v=5.52&access_token=' + access_token
    try:
        data = requests.get(url)
    except RequestException:
        print('Something goes wrong.')
        return None

    if data.status_code == 200:
        data_json = json.loads(data.text)
    else:
        print(f'Response from server not 200 but {data.status_code}')
        return None

    #Теперь получим информацию о полученных пользователях

    friends_list = data_json['response']['items']

    friends_data = []
    for friend in friends_list:
        friend_url = f'https://api.vk.com/method/users.get?user_id={friend}&v=5.52&access_token={access_token}'
        try:
            data_temp = requests.get(friend_url)
        except RequestException:
            print('Something goes wrong.')
        if data_temp.status_code == 200:
            friends_data.append(json.loads(data_temp.text))
        else:
            print(f'Response from server not 200 but {data_temp.status_code}')
        time.sleep(0.5) #инче он начинает ругаться too many requests per second
    
    return data_json, friends_data

data = get_list_of_friends(ACCESS_TOKEN)

if data:
    with open('Friends_data.json', 'w') as f:
        f.write(json.dumps(data))
        print('Success!')
else:
    print('None data passed')
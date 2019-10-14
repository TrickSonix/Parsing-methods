import requests
import json

def user_repos(username):

    url = 'https://api.github.com/users/' + username + '/repos'
    try:
        data = requests.get(url)
    except RequestException:
        print('Something goes wrong.')
        return None
    if data.status_code == 200:
        return json.loads(data.text)
    else:
        print(f'Response from server not 200 but {data.status_code}')
        return None



user = 'TrickSonix'
data_json = user_repos(user)

if data_json:
    for item in data_json:
        print(item['name'])
    with open(f'{user}_repos.json', 'w') as f:
        f.write(json.dumps(data_json))
else:
    print('Data is None')

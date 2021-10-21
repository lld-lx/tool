import requests
import json
url = "https://api.lolicon.app/setu/v2"

headers = {
        'Content-Type': 'application/json'
    }

data = {
    'r18': 1,
    'num': 1,
    'uid': None,
    'size': ["small"],
    'proxy': 'i.pixiv.cat',
    'dsc': False

}
proxies = {
    "https": "https://127.0.0.1:8088",
    "http": "http://127.0.0.1:8088"
}

result = requests.post(url=url, headers=headers, data=json.dumps(data), proxies=proxies, verify=False)
print(result.json())

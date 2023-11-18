from pprint import pprint

import requests

API_KEY = "sample"  # 여러분의 API 인증키로 바꿔주세요.
API_URL = f"http://ecos.bok.or.kr/api/"

service = f"StatisticSearch/{API_KEY}/json/kr/"
params = f"1/1/722Y001/D/20110101/20111231/0101000"
req_url = API_URL + service + params
print(req_url)

resp = requests.get(req_url)
parsed = resp.json()
pprint(parsed)

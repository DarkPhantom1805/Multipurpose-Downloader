import requests

cookies = {
    'tvshow': 'mdlcem1r494ukm3se32e843fu2',
    'token': '63a38cc315e85',
}

headers = {
    'authority': 'gogohd.pro',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    # 'cookie': 'tvshow=mdlcem1r494ukm3se32e843fu2; token=63a38cc315e85',
    'referer': 'https://gogohd.pro/download?id=MTkzNTU3&typesub=Gogoanime-SUB&title=Chainsaw+Man+Episode+1',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

params = {
    'id': 'MTkzNTU3',
    'typesub': 'Gogoanime-SUB',
    'title': 'Chainsaw Man Episode 1',
}

response = requests.head('https://gogohd.pro/download', params=params, cookies=cookies, headers=headers)
print(response.text)
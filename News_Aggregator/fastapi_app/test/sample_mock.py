import requests


def len_joke():
    return len(get_joke())


def get_joke():
    url = "http://api.icndb.com/jokes/random"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['value']['jokes']
    else:
        return "No Jokes"

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


def get_numbers():
    a = int(input("1 st number"))
    b = int(input("2 nd number"))
    return [a, b]


def add_numbers():
    a, b = get_numbers()
    return a + b


if __name__ == "__main__":
    add_numbers()

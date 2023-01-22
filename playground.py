import requests
import dotenv

alphavantage_api_key = dotenv.dotenv_values("python.env").get('alphavantage_api_key')

searched_string = input("Which company interests You?")

symbol_search_params = {
    'function': 'SYMBOL_SEARCH',
    'keywords': searched_string,
    'apikey': alphavantage_api_key
}


symbol_finder = requests.get('https://www.alphavantage.co/query', params=symbol_search_params)
if len(symbol_finder.json()['bestMatches']) > 1:
    for num, i in enumerate(symbol_finder.json()['bestMatches']):
        print(f"{num + 1}.", i['2. name'], i['4. region'])
    try:
        choice = int(input("Which of following is correct?"))
    except ValueError:
        print("You should choose a number, corresponding to the company")
    else:
        print(symbol_finder.json()['bestMatches'][choice-1]['1. symbol'])
else:
    print(symbol_finder.json()['2. name'], symbol_finder.json()['1. symbol'])
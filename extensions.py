import requests
import json
from config import keys, API_KEY

class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        # Проверка на одинаковые валюты
        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')
    
        # Получаем коды валют
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}')
        
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}')

        # Проверяем количество и знак
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}')

        if amount <= 0:
            raise APIException(f'Количество должно быть положительным числом')        
        
        # Запрос к API
        response = requests.get(f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_ticker}')
        data = response.json()
                       
        # Получаем курс и возвращаем сумму
        rate = data['conversion_rates'][quote_ticker]
        return amount * rate
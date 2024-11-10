import requests
from cachetools import cached, TTLCache
from ratelimit import limits, sleep_and_retry

ONE_MINUTE = 60
cache = TTLCache(maxsize=100, ttl=300)  # by this, we are carching the results for 5 minutes

@sleep_and_retry
@limits(calls=10, period=ONE_MINUTE)
@cached(cache)
def get_crypto_price(crypto_id="bitcoin", currency="usd"):
    """
    Fetches the current price of the specified cryptocurrency in the specified currency.

    Args:
        crypto_id (str): The ID of the cryptocurrency (e.g., 'bitcoin', 'ethereum').
        currency (str): The fiat currency to compare against (e.g., 'usd', 'eur').

    Returns:
        float: The current price.

    Raises:
        HTTPError: If an HTTP error occurs during the API call.
        Exception: For other exceptions.
    """
    API_URL = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': crypto_id,
        'vs_currencies': currency
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        price = data.get(crypto_id, {}).get(currency)
        if price is None:
            raise ValueError(f"Price not found for {crypto_id} in {currency}")
        return price
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise
    except Exception as err:
        print(f"Other error occurred: {err}")
        raise

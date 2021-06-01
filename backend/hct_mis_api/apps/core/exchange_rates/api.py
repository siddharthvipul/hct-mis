import logging
import os

from requests import session
from requests.adapters import HTTPAdapter
from urllib3 import Retry


logger = logging.getLogger(__name__)


class ExchangeRateAPI:
    def __init__(self, api_key: str = None, api_url: str = None):
        self.api_key = api_key or os.getenv("EXCHANGE_RATES_API_KEY")
        self.api_url = api_url or os.getenv(
            "EXCHANGE_RATES_API_URL", "https://uniapis.unicef.org/biapi/v1/exchangerates"
        )

        if self.api_key is None:
            raise ValueError("Missing Ocp Apim Subscription Key")

        self._client = session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504], method_whitelist=False)
        self._client.mount(self.api_url, HTTPAdapter(max_retries=retries))
        self._client.headers.update({"Ocp-Apim-Subscription-Key": self.api_key})

    def fetch_exchange_rates(self, with_history: bool = True) -> dict:
        params = {}
        if with_history is True:
            params["history"] = "yes"
        response = self._client.get(self.api_url, params=params)

        try:
            response.raise_for_status()
        except Exception as e:
            logger.exception(e)
            raise

        return response.json()

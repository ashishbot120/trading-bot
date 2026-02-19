import hmac
import hashlib
import time
import urllib.parse
from typing import Any, Dict, Optional

import requests


class BinanceFuturesTestnetClient:
    """
    Minimal REST client for Binance Futures USDT-M Testnet.
    Base URL required by task: https://testnet.binancefuture.com
    Orders endpoint: /fapi/v1/order
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://testnet.binancefuture.com",
        timeout: float = 15.0,
    ):
        if not api_key or not api_secret:
            raise ValueError("API key/secret missing.")
        self.api_key = api_key
        self.api_secret = api_secret.encode("utf-8")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _sign_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # Binance requires timestamp & signature for signed endpoints
        params = dict(params)
        params["timestamp"] = int(time.time() * 1000)

        query = urllib.parse.urlencode(params, doseq=True)
        signature = hmac.new(self.api_secret, query.encode("utf-8"), hashlib.sha256).hexdigest()
        params["signature"] = signature
        return params

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        params = params or {}

        signed_params = self._sign_params(params)

        resp = self.session.request(
            method=method.upper(),
            url=url,
            params=signed_params,
            timeout=self.timeout,
        )

        # Raise good errors with server response
        try:
            data = resp.json()
        except Exception:
            data = {"raw": resp.text}

        if resp.status_code >= 400:
            code = data.get("code")
            msg = data.get("msg")
            raise RuntimeError(f"Binance API error {resp.status_code}: code={code}, msg={msg}, body={data}")

        return data

    def place_order(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # POST /fapi/v1/order
        return self._request("POST", "/fapi/v1/order", params=params)
    
    def get_exchange_info(self) -> dict:
        url = f"{self.base_url}/fapi/v1/exchangeInfo"
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def get_mark_price(self, symbol: str) -> dict:
        url = f"{self.base_url}/fapi/v1/premiumIndex"
        resp = self.session.get(url, params={"symbol": symbol}, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()


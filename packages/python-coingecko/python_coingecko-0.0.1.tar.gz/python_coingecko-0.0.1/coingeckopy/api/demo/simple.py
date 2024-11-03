from typing import cast

from coingeckopy.utils import CoinGeckoApiUrls, CoinGeckoRequestParams, IHttp


class SimpleClient:
    def __init__(self, http: IHttp) -> None:
        self.http = http

    def coin_price_by_id(self, *, request: CoinGeckoRequestParams) -> dict:
        "Query the prices of one or more coins by using their unique Coin API IDs"
        response = self.http.send(path=CoinGeckoApiUrls.PRICE, **request)

        return cast(dict, response)

    def coin_price_by_token(
        self, *, asset_id: str, request: CoinGeckoRequestParams
    ) -> dict:
        "Query a token price by using token contract address."
        path = CoinGeckoApiUrls.TOKEN_PRICE.format(id=asset_id)
        response = self.http.send(path=path, **request)

        return cast(dict, response)

    def supported_vs_currencies(self) -> list:
        "Query all the supported currencies on CoinGecko."
        response = self.http.send(path=CoinGeckoApiUrls.SUPPORTED_CURRENCIES)

        return cast(list, response)

from typing import cast

from coingeckopy.utils import CoinGeckoApiUrls, CoinGeckoRequestParams, IHttp


class SearchClient:
    def __init__(self, http: IHttp) -> None:
        self.http = http

    def search(self, *, request: CoinGeckoRequestParams) -> dict:
        "Search for coins, categories and markets listed on CoinGecko."
        response = self.http.send(path=CoinGeckoApiUrls.SEARCH, **request)

        return cast(dict, response)

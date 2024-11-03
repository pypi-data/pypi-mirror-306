from typing import cast

from coingeckopy.utils import CoinGeckoApiUrls, IHttp


class PingClient:
    def __init__(self, http: IHttp) -> None:
        self.http = http

    def ping(self) -> dict:
        "Check the API server status"
        response = self.http.send(path=CoinGeckoApiUrls.PING)

        return cast(dict, response)

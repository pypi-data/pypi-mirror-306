from typing import cast

from coingeckopy.utils import CoinGeckoApiUrls, IHttp


class GlobalClient:
    def __init__(self, http: IHttp) -> None:
        self.http = http

    def global_market(self) -> dict:
        "query cryptocurrency global data including active cryptocurrencies, markets, total crypto market cap and etc."
        response = self.http.send(path=CoinGeckoApiUrls.GLOBAL)

        return cast(dict, response)

    def global_defi_market(self) -> dict:
        "query top 100 cryptocurrency global decentralized finance (defi) data including defi market cap, trading volume."
        response = self.http.send(path=CoinGeckoApiUrls.GLOBAL_DEFI)

        return cast(dict, response)

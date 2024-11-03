from typing import cast

from coingeckopy.utils import CoinGeckoApiUrls, CoinGeckoRequestParams, IHttp


class CoinsClient:
    def __init__(self, http: IHttp) -> None:
        self.http = http

    def coins_list(self, *, request: CoinGeckoRequestParams) -> list:
        "Query all the supported coins on CoinGecko with coins id, name and symbol."
        response = self.http.send(path=CoinGeckoApiUrls.COINS_LIST, **request)

        return cast(list, response)

    def coins_markets(self, *, request: CoinGeckoRequestParams) -> list:
        "Query all the supported coins with price, market cap, volume and market related data."
        response = self.http.send(path=CoinGeckoApiUrls.COINS_MARKETS, **request)

        return cast(list, response)

    def coin_by_id(self, *, coin_id: str, request: CoinGeckoRequestParams) -> dict:
        "Query all the coin data of a coin (name, price, market .... including exchange tickers) on CoinGecko coin page based on a particular coin id."
        path = CoinGeckoApiUrls.COIN.format(id=coin_id)
        response = self.http.send(path=path, **request)

        return cast(dict, response)

    def coin_tickers_by_id(
        self, *, coin_id: str, request: CoinGeckoRequestParams
    ) -> dict:
        "Query the coin tickers on both centralized exchange (cex) and decentralized exchange (dex) based on a particular coin id."
        path = CoinGeckoApiUrls.COIN_TICKERS.format(id=coin_id)
        response = self.http.send(path=path, **request)

        return cast(dict, response)

    def coin_history_by_id(
        self, *, coin_id: str, request: CoinGeckoRequestParams
    ) -> dict:
        "Query the historical data (price, market cap, 24hrs volume, etc) at a given date for a coin based on a particular coin id."
        path = CoinGeckoApiUrls.COIN_HISTORY.format(id=coin_id)
        response = self.http.send(path=path, **request)

        return cast(dict, response)

    def coin_history_chart_by_id(
        self, *, coin_id: str, request: CoinGeckoRequestParams
    ) -> dict:
        "Query the historical price, market cap, volume, and total supply at a given date for a coin in a particular currency based on a particular coin id."
        path = CoinGeckoApiUrls.COIN_HISTORY_CHART.format(id=coin_id)
        response = self.http.send(path=path, **request)

        return cast(dict, response)

    def coin_history_chart_range_by_id(
        self, *, coin_id: str, request: CoinGeckoRequestParams
    ) -> dict:
        "Get the historical chart data of a coin within certain time range in UNIX along with price, market cap and 24hrs volume based on particular coin id."
        path = CoinGeckoApiUrls.COIN_HISTORY_TIME_RANGE.format(id=coin_id)
        response = self.http.send(path=path, **request)

        return cast(dict, response)

    def coin_ohlc_by_id(self, *, coin_id: str, request: CoinGeckoRequestParams) -> list:
        "Get the historical OHLC (Open, High, Low, Close) of a coin within a range in UNIX timestamp."
        path = CoinGeckoApiUrls.COIN_OHLC.format(id=coin_id)
        response = self.http.send(path=path, **request)

        return cast(list, response)

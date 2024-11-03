from typing import cast

from coingeckopy.utils import CoinGeckoApiUrls, CoinGeckoRequestParams, IHttp


class ExchangesClient:
    def __init__(self, http: IHttp) -> None:
        self.http = http

    def exchanges_list(self, *, request: CoinGeckoRequestParams) -> list:
        "Query all the supported exchanges with exchanges’ data (id, name, country, .... etc) that have active trading volumes on CoinGecko."
        response = self.http.send(path=CoinGeckoApiUrls.EXCHANGES, **request)

        return cast(list, response)

    def exchanges_list_id_map(self) -> list:
        "Query all the supported coins with price, market cap, volume and market related data."
        response = self.http.send(path=CoinGeckoApiUrls.EXCHANGES_LIST)

        return cast(list, response)

    def exchange_by_id(self, *, exchange_id: str) -> dict:
        "Query all the coin data of a coin (name, price, market .... including exchange tickers) on CoinGecko coin page based on a particular coin id."
        path = CoinGeckoApiUrls.EXCHANGE.format(id=exchange_id)
        response = self.http.send(path=path)

        return cast(dict, response)

    def exchange_tickers_by_id(
        self, *, exchange_id: str, request: CoinGeckoRequestParams
    ) -> dict:
        "Query exchange's tickers based on exchange’s id."
        path = CoinGeckoApiUrls.EXCHANGE_TICKERS.format(id=exchange_id)
        response = self.http.send(path=path, **request)

        return cast(dict, response)

    def exchange_volume_chart_by_id(
        self, *, exchange_id: str, request: CoinGeckoRequestParams
    ) -> dict:
        "Query the historical volume chart data with time in UNIX and trading volume data in BTC based on exchange’s id."
        path = CoinGeckoApiUrls.EXCHANGE_VOLUME_CHART.format(id=exchange_id)
        response = self.http.send(path=path, **request)

        return cast(dict, response)

from typing import Optional, cast

from coingeckopy.utils import CoinGeckoApiUrls, CoinGeckoRequestParams, IHttp


class DerivativesClient:
    def __init__(self, http: IHttp) -> None:
        self.http = http

    def ticker_list(self) -> list:
        "Query all the tickers from derivatives exchanges on CoinGecko."
        response = self.http.send(path=CoinGeckoApiUrls.DERIVATIVES_TICKERS)

        return cast(list, response)

    def exchanges_list_with_data(self, *, request: CoinGeckoRequestParams) -> list:
        "Query all the derivatives exchanges with related data (id, name, open interest, .... etc) on CoinGecko."
        response = self.http.send(
            path=CoinGeckoApiUrls.DERIVATIVES_EXCHANGES, **request
        )

        return cast(list, response)

    def exchange_by_id(
        self, *, exchange_id: str, request: Optional[CoinGeckoRequestParams] = None
    ) -> dict:
        "Query the derivatives exchange’s related data (id, name, open interest, .... etc) based on the exchanges’ id."
        path = CoinGeckoApiUrls.DERIVATIVES_EXCHANGE.format(id=exchange_id)
        data = request or {}
        response = self.http.send(path=path, **data)

        return cast(dict, response)

    def exchanges_list_id_map(self) -> list:
        "Query all the derivatives exchanges with id and name on CoinGecko."
        response = self.http.send(path=CoinGeckoApiUrls.DERIVATIVES_EXCHANGE_LIST)

        return cast(list, response)

from coingeckopy.clients.demo import CoinGeckoDemoClient
from coingeckopy.clients.pro import CoinGeckoProClient
from coingeckopy.utils import (
    DEMO_COIN_GECKO_API_URL,
    PRO_COIN_GECKO_API_URL,
    RequestsClient,
)
from coingeckopy.utils.exceptions import CoinGeckoClientError
from coingeckopy.utils.helpers import get_client_api_methods


class CoinGecko:
    """Main CoinGecko API Client"""

    def __init__(
        self, api_key: str = "", is_pro: bool = False, use_onchain: bool = False
    ) -> None:
        if not is_pro and use_onchain:
            raise CoinGeckoClientError("Onchain data is only available for pro API")

        header_name = "x-cg-pro-api-key" if is_pro else "x-cg-demo-api-key"
        url = PRO_COIN_GECKO_API_URL if is_pro else DEMO_COIN_GECKO_API_URL
        http = RequestsClient(base_url=url, headers={header_name: api_key})
        client = CoinGeckoProClient if is_pro else CoinGeckoDemoClient

        attr_list = get_client_api_methods(client=client)

        for attr in attr_list:
            setattr(self, attr, getattr(client(http), attr))

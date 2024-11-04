# kaziro/__init__.py

from typing import Callable, List, Literal, Optional

import urllib3

from .api.generated.kaziro import ApiClient, Configuration
from .api.generated.kaziro.api import MarketApi, OrderApi, PositionApi, UserApi, WalletApi
from .api.generated.kaziro.models import (
    AcceptOrdersRequest,
    AcceptOrdersResponse,
    MarketCreationResponse,
    MarketDetail,
    MarketPriceHistoryResponse,
    MarketRetrievalResponse,
    OpenOrdersResponse,
    OrderPair,
    OrderRequest,
    PlaceOrderResponse,
    PositionResponse,
    RequestDefaultRepliesRequest,
    RequestDefaultRepliesResponse,
    UserProfileResponse,
    WalletInfoResponse,
)
from .template.base_replier import BaseReplierTemplate  # noqa: F401
from .websocket.client import KaziroWebSocket


class Kaziro:
    def __init__(self, api_key: str, api_url: str = "https://api.kaziro.xyz", ws_url: str = "wss://ws.kaziro.xyz", verbose: bool = False, verify_ssl: bool = True):
        self.api_key = api_key
        self.api_url = api_url
        self.ws_url = ws_url
        self.verbose = verbose
        self.verify_ssl = verify_ssl
        # Initialize Configuration and ApiClient
        self.config = Configuration(host=self.api_url, api_key={"APIKeyHeader": self.api_key})
        self.config.verify_ssl = verify_ssl
        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.api_client = ApiClient(configuration=self.config)

        # Initialize API classes
        self.user = self.User(self.api_client)
        self.market = self.Market(self.api_client)
        self.order = self.Order(self.api_client)
        self.position = self.Position(self.api_client)
        self.wallet = self.Wallet(self.api_client)

        # Initialize WebSocket
        self.ws = KaziroWebSocket(self.ws_url, self.api_key, verbose=self.verbose, verify_ssl=self.verify_ssl)

    class User:
        def __init__(self, api_client: ApiClient):
            self.api = UserApi(api_client)

        def retrieve(self) -> UserProfileResponse:
            return self.api.profile_endpoint_v1_user_retrieve_get()

    class Market:
        def __init__(self, api_client: ApiClient):
            self.api = MarketApi(api_client)

        def create(self, market_details: List[MarketDetail]) -> MarketCreationResponse:
            return self.api.create_market_endpoint_v1_exchange_market_create_post(market_details)

        def create_single(self, detail: str) -> MarketCreationResponse:
            market_detail = MarketDetail(detail=detail)
            response = self.api.create_market_endpoint_v1_exchange_market_create_post([market_detail])
            return response

        def retrieve(
            self,
            market_ids: Optional[List[str]] = None,
            statuses: Optional[List[str]] = None,
            tags: Optional[List[str]] = None,
            creator_id: Optional[str] = None,
            search_query: Optional[str] = None,
            sort_by: Optional[str] = None,
            sort_direction: Optional[str] = None,
            bucket: Optional[str] = None,
            page: Optional[int] = None,
        ) -> MarketRetrievalResponse:
            return self.api.retrieve_markets_endpoint_v1_exchange_market_retrieve_get(market_ids, statuses, tags, creator_id, search_query, sort_by, sort_direction, bucket, page)

        def retrieve_ohlc(self, market_ids: List[str]) -> MarketPriceHistoryResponse:
            return self.api.retrieve_ohlc_endpoint_v1_exchange_market_retrieve_ohlc_get(market_ids)

        def retrieve_ohlc_single(self, market_id: str) -> MarketPriceHistoryResponse:
            return self.api.retrieve_ohlc_endpoint_v1_exchange_market_retrieve_ohlc_get([market_id])

    class Order:
        def __init__(self, api_client: ApiClient):
            self.api = OrderApi(api_client)

        def create(self, orders: List[OrderRequest]) -> PlaceOrderResponse:
            return self.api.create_market_endpoint_v1_exchange_order_create_post(orders)

        def create_single_request(self, size: float, market_id: str, outcome: Literal[1, 2]) -> PlaceOrderResponse:
            order = OrderRequest(size=size, market_id=market_id, order_type="MARKET_REQUEST", outcome=outcome)
            return self.api.create_market_endpoint_v1_exchange_order_create_post([order])

        def create_single_reply(self, request_id: Optional[str], probability: float, outcome: Literal[1, 2]) -> PlaceOrderResponse:
            order = OrderRequest(request_id=request_id, probability=probability, order_type="MARKET_REPLY", outcome=outcome)
            return self.api.create_market_endpoint_v1_exchange_order_create_post([order])

        def retrieve(self, order_ids: Optional[List[str]] = None, market_ids: Optional[List[str]] = None, filter_user: bool = False) -> OpenOrdersResponse:
            return self.api.get_open_orders_endpoint_v1_exchange_order_retrieve_get(order_ids, market_ids, filter_user)

        def accept(self, orders: List[OrderPair]) -> AcceptOrdersResponse:
            accept_orders_request = AcceptOrdersRequest(orders=orders)
            return self.api.accept_orders_endpoint_v1_exchange_order_accept_post(accept_orders_request)

        def accept_single(self, request_id: str, reply_id: str) -> AcceptOrdersResponse:
            order_pair = OrderPair(request_id=request_id, reply_id=reply_id)
            return self.accept([order_pair])

        def request_default_replies(self, order_ids: List[str]) -> RequestDefaultRepliesResponse:
            request_default_replies_request = RequestDefaultRepliesRequest(order_ids=order_ids)
            return self.api.request_default_replies_endpoint_v1_exchange_order_temporary_reply_post(request_default_replies_request)

        def request_default_reply_single(self, order_id: str) -> RequestDefaultRepliesResponse:
            return self.request_default_replies([order_id])

    class Position:
        def __init__(self, api_client: ApiClient):
            self.api = PositionApi(api_client)

        def retrieve(self, status: Optional[str] = None, page: Optional[int] = None, sort_order: Optional[str] = None) -> PositionResponse:
            return self.api.get_positions_v1_exchange_position_retrieve_get(status=status, page=page, sort_order=sort_order)

    class Wallet:
        def __init__(self, api_client: ApiClient):
            self.api = WalletApi(api_client)

        def retrieve(self) -> WalletInfoResponse:
            return self.api.wallet_info_endpoint_v1_wallet_retrieve_get()

    def connect_websocket(self):
        self.ws.connect()

    def subscribe_websocket(self, channel: str):
        self.ws.subscribe(channel)

    def set_websocket_callback(self, callback: Callable[[str], None]):
        self.ws.set_message_callback(callback)


__all__ = ["Kaziro"]

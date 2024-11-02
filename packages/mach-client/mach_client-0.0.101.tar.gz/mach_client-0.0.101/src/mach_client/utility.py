import functools

from web3 import AsyncWeb3
from web3.contract import AsyncContract
from web3.middleware import ExtraDataToPOAMiddleware
from web3.providers import (
    AsyncBaseProvider,
    AsyncHTTPProvider,
    AsyncIPCProvider,
    WebSocketProvider,
)

from . import config
from .data_types import ChainId, Token
from .client import client


def make_provider(endpoint_uri: str) -> AsyncBaseProvider:
    if endpoint_uri.startswith("ws://") or endpoint_uri.startswith("wss://"):
        return WebSocketProvider(endpoint_uri)
    elif endpoint_uri.startswith("http://") or endpoint_uri.startswith("https://"):
        return AsyncHTTPProvider(endpoint_uri)
    elif endpoint_uri.endswith(".ipc"):
        return AsyncIPCProvider(endpoint_uri)
    else:
        raise ValueError(f"Invalid endpoint URI: {endpoint_uri}")


@functools.cache
def _make_w3(chain: ChainId) -> AsyncWeb3:
    provider = make_provider(config.endpoint_uris[chain])
    w3 = AsyncWeb3(provider)
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    return w3


async def make_w3(chain: ChainId) -> AsyncWeb3:
    w3 = _make_w3(chain)
    assert await w3.is_connected()
    return w3


def make_token_contract(w3: AsyncWeb3, token: Token) -> AsyncContract:
    return w3.eth.contract(
        address=AsyncWeb3.to_checksum_address(token.contract_address),
        abi=config.erc20_abi,
    )


def make_order_book_contract(w3: AsyncWeb3, token: Token) -> AsyncContract:
    return w3.eth.contract(
        address=client.deployments[token.chain.id]["contracts"]["order_book"],
        abi=config.order_book_abi,
    )

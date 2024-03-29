from unittest.mock import MagicMock

import pytest
from freqtrade_client import FtRestClient


def get_rest_client():
    client = FtRestClient('http://localhost:8080', 'freqtrader', 'password')
    client._session = MagicMock()
    request_mock = MagicMock()
    client._session.request = request_mock
    return client, request_mock


def test_FtRestClient_init():
    client = FtRestClient('http://localhost:8080', 'freqtrader', 'password')
    assert client is not None
    assert client._serverurl == 'http://localhost:8080'
    assert client._session is not None
    assert client._session.auth is not None
    assert client._session.auth == ('freqtrader', 'password')


@pytest.mark.parametrize('method', ['GET', 'POST', 'DELETE'])
def test_FtRestClient_call(method):
    client, mock = get_rest_client()
    client._call(method, '/dummytest')
    assert mock.call_count == 1

    getattr(client, f"_{method.lower()}")('/dummytest')
    assert mock.call_count == 2


@pytest.mark.parametrize('method,args', [
    ('start', []),
    ('stop', []),
    ('stopbuy', []),
    ('reload_config', []),
    ('balance', []),
    ('count', []),
    ('entries', []),
    ('exits', []),
    ('mix_tags', []),
    ('locks', []),
    ('delete_lock', [2]),
    ('daily', []),
    ('daily', [15]),
    ('weekly', []),
    ('weekly', [15]),
    ('monthly', []),
    ('monthly', [12]),
    ('edge', []),
    ('profit', []),
    ('stats', []),
    ('performance', []),
    ('status', []),
    ('version', []),
    ('show_config', []),
    ('ping', []),
    ('logs', []),
    ('logs', [55]),
    ('trades', []),
    ('trades', [5]),
    ('trades', [5, 5]),  # With offset
    ('trade', [1]),
    ('delete_trade', [1]),
    ('cancel_open_order', [1]),
    ('whitelist', []),
    ('blacklist', ['XRP/USDT']),
    ('blacklist', ['XRP/USDT', 'BTC/USDT']),
    ('forcebuy', ['XRP/USDT']),
    ('forcebuy', ['XRP/USDT', 1.5]),
    ('forceenter', ['XRP/USDT', 'short']),
    ('forceenter', ['XRP/USDT', 'short', 1.5]),
    ('forceexit', [1]),
    ('forceexit', [1, 'limit']),
    ('forceexit', [1, 'limit', 100]),
    ('strategies', []),
    ('strategy', ['sampleStrategy']),
    ('pairlists_available', []),
    ('plot_config', []),
    ('available_pairs', []),
    ('available_pairs', ['5m']),
    ('pair_candles', ['XRP/USDT', '5m']),
    ('pair_candles', ['XRP/USDT', '5m', 500]),
    ('pair_history', ['XRP/USDT', '5m', 'SampleStrategy']),
    ('sysinfo', []),
    ('health', []),
])
def test_FtRestClient_call_explicit_methods(method, args):
    client, mock = get_rest_client()
    exec = getattr(client, method)
    exec(*args)
    assert mock.call_count == 1

import json
import logging

import pytest

from jquant import InstrumentKind, PlatformClient

_platform = "futu.hk"
_inst = "HK.00700"
_insts = [_inst]
_strategy = "GridStrategy"
_investor = "PROD001"


@pytest.fixture
def pc() -> PlatformClient:
    return PlatformClient(
        _strategy,
        "localhost:8081",
        # "192.168.1.200:18081",
        # TEST02
        # "192.168.1.200:48081",
        # "172.16.2.41:8081",
        metadata=[
            ("initial-metadata-1", "The value should be str"),
            ("authorization", "gRPC Python is great"),
        ],
    )


def test_get_ticker(pc):
    reply = pc.get_ticker(platform=_platform, instrument=_inst)
    print(f"recv from server, result={reply}")


def test_get_tickers(pc):
    reply = pc.get_tickers(platforms=[_platform], instruments=_insts)
    print(f"recv from server, result={reply}")


def test_get_kline(pc):
    reply = pc.get_kline(platform=_platform, instrument=_inst, period="1m")
    print(f"recv from server, result={reply}")


def test_get_position(pc):
    reply = pc.get_position(
        platform=_platform,
    )
    print(f"recv from server, result={reply}")


def test_get_instrument(pc):
    reply = pc.get_instruments(
        platform=_platform,
        kinds=[InstrumentKind.FUTURE],
        instruments=_insts,
    )
    print(f"recv from server, result={reply}")


def test_get_config(pc):
    reply = pc.get_config(
        platform=_platform,
        strategy=_strategy,
    )
    print(f"recv from server, reply={reply}")

    # 获取策略配置
    strategy = json.loads(reply.get("strategy", "{}"))
    print(f"strategy={strategy}")

    # 获取该策略的合约配置
    instruments = json.loads(reply.get("instruments", "{}"))
    print(f"instruments={instruments}")


def test_get_order(pc):
    reply = pc.get_order(
        platform=_platform,
        instrument=_inst,
        client_order_id="84041793665",
    )
    print(f"recv from server, result={reply}")


def test_get_orders(pc):
    orders = pc.get_orders(
        platform=_platform,
        instruments=_insts,
        investor=_investor,
        strategy=_strategy,
    )
    # print(f"recv from server, result={orders}")
    for order in orders:
        print(f"order={order}")


def test_cancel(pc):
    reply = pc.cancel(
        platform=_platform,
        instrument=_inst,
        client_order_ids=["89745522817"],
    )
    print(f"recv from server, result={reply}")


def test_buy(pc):
    reply = pc.buy(
        platform=_platform,
        instrument=_inst,
        price="102.5",
        amount="1",
        investor=_investor,
        strategy=_strategy,
        source="01",
        tag="01",
        # VolumeCondition="3",
    )
    print(f"recv from server, result={reply}")


def test_close_buy(pc):
    reply = pc.close_buy(
        platform=_platform,
        instrument=_inst,
        price="102",
        amount="1",
        investor=_investor,
        strategy=_strategy,
    )
    print(f"recv from server, result={reply}")


def test_sell(pc):
    reply = pc.sell(
        platform=_platform,
        instrument=_inst,
        price="559",
        amount="1",
        investor=_investor,
        strategy=_strategy,
        source="01",
        tag="01",
        # VolumeCondition="3",
    )
    print(f"recv from server, result={reply}")


def test_close_sell(pc):
    reply = pc.close_sell(
        platform=_platform,
        instrument=_inst,
        price="3832",
        amount="1",
        investor=_investor,
        strategy=_strategy,
        CombOffsetFlag="3",
    )
    print(f"recv from server, result={reply}")


def test_subscribe_order(pc):
    pc.subscribe_order(
        platform=_platform,
        instruments=[_inst],
        investor=_investor,
        strategy=_strategy,
        handler=on_order,
    )


def on_order(orders):
    for order in orders:
        print(f"order={order}")


def test_subscribe_ticker(pc):
    pc.subscribe_tick(
        platforms=[_platform],
        instruments=_insts,
        handler=on_tick,
    )


def on_tick(ticker):
    # print(f"recv from server, ticker={ticker}")
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # t.test_get_ticker()
    # t.test_get_order()
    # t.test_get_orders()
    # t.test_buy()
    # t.test_closebuy()
    # t.test_cancel()
    # t.test_get_instrument()
    t.test_subscribe_ticker()
    # t.test_subscribe_order()
    # t.test_get_position()

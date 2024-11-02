import json
import logging
import logging.config
import os
import time

import pytest

from jquant import InstrumentKind, PlatformClient

_platform = "ctp.future"
_inst = "SPD SA502&SA509"
_insts = [_inst, "SPD FG502&FG503", "FG502"]
_strategy = "GridStrategy"
_investor = "PROD001"


def platformClient():
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


@pytest.fixture
def pc():
    pc = platformClient()
    yield pc
    pc.close()


def test_get_ticker(pc):
    reply = pc.get_ticker(platform=_platform, instrument=_inst)
    print(f"recv from server, result={reply}")


def test_get_tickers(pc):
    reply = pc.get_tickers(platforms=["ctp.future"], instruments=_insts)
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
        client_order_ids=["86000009281"],
    )
    print(f"recv from server, result={reply}")


def test_buy(pc):
    reply = pc.buy(
        platform=_platform,
        instrument=_inst,
        price="573.2",
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
        price="572.82",
        amount="1",
        investor=_investor,
        strategy=_strategy,
        CombOffsetFlag="3",
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
        source="01",
        tag="xxx",
    )


def on_order(orders):
    for order in orders:
        print(f"order={order}")


def test_subscribe_ticker(pc):
    pc.subscribe_tick(
        platforms=["ctp.future"],
        instruments=_insts,
        handler=on_tick,
    )


def on_tick(ticker):
    # print(f"recv from server, ticker={ticker}")
    pass


def test_subscribe_instruments(pc):
    pc.subscribe_instruments(
        platform=_platform,
        instruments=["SPC a2501&m2501"],
        handler=on_instruments,
    )


def on_instruments(instruments):
    # print(f"recv from server, instruments={ticker}")
    pass


def test_ping(pc: PlatformClient):
    reply = pc.ping()
    for r in reply:
        print(f"recv from server, result={r}")
        time.sleep(1)


def test_ping2(pc: PlatformClient):
    pc.ping(handler=on_tick)


if __name__ == "__main__":
    os.environ["GRPC_TRACE"] = "client_channel,http_keepalive"
    os.environ["GRPC_VERBOSITY"] = "DEBUG"
    logging.basicConfig(level=logging.DEBUG)
    pc = platformClient()
    # test_ping(pc)
    # test_get_ticker(pc)
    # t.test_get_order()
    # t.test_get_orders()
    # t.test_buy()
    # t.test_closebuy()
    # t.test_cancel()
    # t.test_get_instrument()
    test_subscribe_ticker(pc)
    # test_subscribe_instruments(pc)
    # t.test_subscribe_order()
    # t.test_get_position()

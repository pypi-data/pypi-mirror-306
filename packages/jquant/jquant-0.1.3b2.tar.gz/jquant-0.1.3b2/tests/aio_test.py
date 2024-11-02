import asyncio
import json
import logging
import logging.config

import pytest

from jquant import InstrumentKind, pb
from jquant.aio import PlatformClient

log = logging.getLogger(__name__)

# @pytest.fixture
# async def channel(event_loop):
#     channel = grpc.aio.insecure_channel("localhost:8081")
#     yield channel
#     await channel.close()


# @pytest.mark.asyncio
# async def grpc_client(channel):
#     return PlatformClient(
#         _strategy,
#         channel,
#         # "192.168.1.200:18081",
#         # TEST02
#         # "192.168.1.200:48081",
#         # "172.16.2.41:8081",
#         metadata=[
#             ("initial-metadata-1", "The value should be str"),
#             ("authorization", "gRPC Python is great"),
#         ],
#     )

import os

_inst = "c2409"
_insts = [_inst]
_strategy = "sp_grid"
_investor = "PROD001"


def platformClient() -> PlatformClient:
    return PlatformClient(
        _strategy,
        "127.0.0.1:8081",
        # "172.16.6.15:8081",
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
async def pc():
    pc = platformClient()
    yield pc
    await pc.close()


async def test_get_ticker(pc):
    reply = await pc.get_ticker(platform="ctp.future", instrument=_inst)
    print(f"recv from server, result={reply}")


async def test_get_tickers(pc):
    reply = await pc.get_tickers(platforms=["ctp.future"], instruments=_insts)
    print(f"recv from server, result={reply}")


async def test_get_kline(pc):
    reply = await pc.get_kline(platform="ctp.future", instrument=_inst, period="1m")
    print(f"recv from server, result={reply}")


async def test_get_position(pc):
    reply = await pc.get_position(
        platform="ctp.future",
    )
    print(f"recv from server, result={reply}")


async def test_get_instrument(pc):
    reply = await pc.get_instruments(
        platform="ctp.future",
        kinds=[InstrumentKind.FUTURE],
        instruments=_insts,
    )
    print(f"recv from server, result={reply}")


async def test_get_config(pc):
    reply = await pc.get_config(
        platform="ctp.future",
        strategy=_strategy,
    )
    print(f"recv from server, reply={reply}")

    # 获取策略配置
    strategy = json.loads(reply.get("strategy", "{}"))
    print(f"strategy={strategy}")

    # 获取该策略的合约配置
    instruments = json.loads(reply.get("instruments", "{}"))
    print(f"instruments={instruments}")


async def test_get_order(pc):
    reply = await pc.get_order(
        platform="ctp.future",
        instrument=_inst,
        client_order_id="84041793665",
    )
    print(f"recv from server, result={reply}")


async def test_get_orders(pc):
    orders = await pc.get_orders(
        platform="ctp.future",
        instruments=_insts,
        investor=_investor,
        strategy=_strategy,
    )
    # print(f"recv from server, result={orders}")
    for order in orders:
        print(f"order={order}")


async def test_cancel(pc):
    reply = await pc.cancel(
        platform="ctp.future",
        instrument=_inst,
        client_order_ids=["86000009281"],
    )
    print(f"recv from server, result={reply}")


async def test_buy(pc):
    reply = await pc.buy(
        platform="ctp.future",
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


async def test_close_buy(pc):
    reply = await pc.close_buy(
        platform="ctp.future",
        instrument=_inst,
        price="572.82",
        amount="1",
        investor=_investor,
        strategy=_strategy,
        CombOffsetFlag="3",
    )
    print(f"recv from server, result={reply}")


async def test_sell(pc):
    reply = await pc.sell(
        platform="ctp.future",
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


async def test_close_sell(pc):
    reply = await pc.close_sell(
        platform="ctp.future",
        instrument=_inst,
        price="3832",
        amount="1",
        investor=_investor,
        strategy=_strategy,
        CombOffsetFlag="3",
    )
    print(f"recv from server, result={reply}")


async def test_subscribe_order(pc):
    iter = await pc.subscribe_order(
        platform="ctp.future",
        instruments=[_inst],
        investor=_investor,
        strategy=_strategy,
        source="01",
        tag="xxx",
    )


async def on_order(self, orders):
    for order in orders:
        print(f"order={order}")


async def test_subscribe_ticker(pc):
    reply_itertor = pc.subscribe_tick(
        platforms=["ctp.future"],
        instruments=_insts,
    )
    async for reply in reply_itertor:
        print(f"recv from server, result={reply}")


async def test_subscribe_instruments(pc):
    reply_itertor = pc.subscribe_instruments(
        platform="ctp.future",
        instruments=["SPD MA502&MA503"],
    )
    async for reply in reply_itertor:
        pass


async def test_ping(pc: PlatformClient):
    print(f"Current event loop: {asyncio.get_event_loop()}")

    async for reply in pc.ping():
        print(f"recv from server, result={reply}")
        await asyncio.sleep(1)


async def main():
    pc = platformClient()
    # await test_ping(pc)
    # t.test_get_ticker()
    # t.test_get_order()
    # t.test_get_orders()
    # t.test_buy()
    # t.test_closebuy()
    # t.test_cancel()
    # await test_get_instrument(pc)
    # t.test_subscribe_ticker()
    await test_subscribe_instruments(pc)
    # t.test_subscribe_order()
    # t.test_get_position()


if __name__ == "__main__":
    os.environ["GRPC_TRACE"] = "client_channel,http_keepalive"
    os.environ["GRPC_VERBOSITY"] = "DEBUG"

    logging.basicConfig(level=logging.DEBUG)

    asyncio.run(main())

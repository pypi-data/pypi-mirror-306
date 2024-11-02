import itertools
from enum import Enum

from google.protobuf import any_pb2 as anypb
from google.protobuf import message

from . import platform_pb2 as pb

"""
grpc.keepalive_time_ms: The period (in milliseconds) after which a keepalive ping is
    sent on the transport.
grpc.keepalive_timeout_ms: The amount of time (in milliseconds) the sender of the keepalive
    ping waits for an acknowledgement. If it does not receive an acknowledgment within this
    time, it will close the connection.
grpc.keepalive_permit_without_calls: If set to 1 (0 : false; 1 : true), allows keepalive
    pings to be sent even if there are no calls in flight.
grpc.http2.max_pings_without_data: How many pings can the client send before needing to
    send a data/header frame.
For more details, check: https://github.com/grpc/grpc/blob/master/doc/keepalive.md
"""
channel_options = [
    # 每30秒发送一次心跳
    ("grpc.keepalive_time_ms", 30000),
    # 5秒内没有收到回应，则认为连接断开
    ("grpc.keepalive_timeout_ms", 5000),
    # 在没有数据传输的情况下，允许发送心跳次数, 0 表示不限制
    ("grpc.http2.max_pings_without_data", 0),
    # 允许在没有数据传输的情况下发送心跳, 1 表示允许
    ("grpc.keepalive_permit_without_calls", 1),
]


class SubscribeMethod(Enum):
    """可用的订阅方法"""

    PING = "ping"
    """心跳"""
    TICKER = "ticker"
    """行情"""
    KLINE = "kline"
    """K线"""
    ORDER = "order"
    """订单"""
    CONFIG = "config"
    """配置"""
    INSTRUMENT = "instrument"
    """合约"""


class InstrumentKind:
    """可用的标的类型"""

    FUTURE = "1"  # 期货
    """期货"""
    OPTION = "2"  # 期权
    """期权"""
    COMBINATION = "3"  # 组合
    """组合"""
    SPOT = "4"  # 即期(现货)
    """即期(现货)"""
    FUTURE_TO_SPOT = "5"  # 期转现
    """期转现"""
    SPOT_OPTION = "6"  # 现货期权
    """现货期权"""
    TAS = "7"  # TAS合约
    """TAS合约"""
    METAL_INDEX = "8"  # 金属指数
    """金属指数"""


class OrderState:
    """订单状态"""

    UNKNOWN = pb.Order.STATE_UNKNOWN

    CREATED = pb.Order.STATE_CREATED
    """创建: 服务端收到订单请求,并入库"""

    SUBMITTED = pb.Order.STATE_SUBMITTED
    """已提交: 已经提交给交易所,并收到交易所提交成功的回报"""

    PARTIAL_FILLED = pb.Order.STATE_PARTIAL_FILLED
    """部分成交"""

    FILLED = pb.Order.STATE_FILLED
    """全部成交"""

    CANCELED = pb.Order.STATE_CANCELED
    """已经撤单"""

    REJECTED = pb.Order.STATE_REJECTED
    """拒绝: 交易所拒绝订单,返回错误信息"""

    EXPIRED = pb.Order.STATE_EXPIRED
    """失效: 订单失效, 隔交易日订单或者其他原因导致订单失效"""


class PositionSide:
    """持仓方向"""

    NET = pb.Position.SIDE_NET
    """净持仓"""
    LONG = pb.Position.SIDE_LONG
    """多头"""
    SHORT = pb.Position.SIDE_SHORT
    """空头"""


_counter = itertools.count(1)


def subscribe_request(
    method: SubscribeMethod, req: message.Message
) -> pb.SubscribeRequest:
    """构造订阅请求

    Args:
        method (SubscribeMethod): 订阅方法
        req (message.Message): 请求参数

    Returns:
        pb.SubscribeRequest: 订阅请求
    """
    any = anypb.Any()
    if req:
        any.Pack(req)
    return pb.SubscribeRequest(
        id=next(_counter),
        method=method.value,
        params=any,
    )

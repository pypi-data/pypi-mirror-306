import logging
import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Generator

import grpc
from google.protobuf import any_pb2 as anypb
from google.protobuf import message

from . import platform_pb2 as pb
from . import platform_pb2_grpc as grpcpb
from ._typing import InstrumentKind, SubscribeMethod, channel_options, subscribe_request

log = logging.getLogger(__name__)


def init_channel(target: str = "localhost:8081") -> grpc.Channel:
    """
    初始化 gRPC 通道。

    Args:
        target (str): 目标地址，默认为 "localhost:8081"。

    Returns:
        grpc.Channel: gRPC 通道对象。
    """
    return grpc.insecure_channel(
        target=target,
        options=channel_options,
        compression=grpc.Compression.Gzip,
    )


def request_generator(q: queue.Queue) -> Generator[pb.SubscribeRequest, None, None]:
    while True:
        try:
            item = q.get()
            q.task_done()
            if item is None:  # 使用 None 作为终止信号
                log.warning(">>>stop iteration")
                break
            yield item

        except StopIteration or GeneratorExit:
            log.info(">>>stop iteration")
            break


class PlatformClient:
    """平台访问客户端

    平台访问的客户端, 通过 grpc 访问后端服务,提供基本的数据流订阅和 grpc 接口调用.

    Attributes:
        name: 客户端名称。
        _metadata(list[tuple]): 元数据列表。
        _executor(ThreadPoolExecutor): 线程池执行器。
        _channel(grpc.Channel): gRPC通道对象。
        _stream(grpcpb.StreamServiceStub): 流服务存根对象。
        _client(grpcpb.ExchangeServiceStub): 交换服务存根对象。

    Examples:
        >>> with PlatformClient("jquant-python", "localhost:8081") as pc:
        >>>     pc.get_ticker("ctp.future", "rb2105")
        >>>     pc.get_tickers(["ctp.future"], ["rb2105", "i2105"])
        >>>     pc.get_kline("ctp.future", "rb2105", "1m")
        >>>     pc.get_position("ctp.future")
        >>>     pc.get_instruments("ctp.future", [InstrumentKind.FUTURE], ["rb2105", "i2105"])
        >>>     pc.get_config("ctp.future", "strategy")
        >>>     pc.get_order("ctp.future", "rb2105", "client_order_id")
        >>>     pc.get_orders("ctp.future", ["rb2105", "i2105"], "investor", "strategy")

    """

    def __init__(
        self,
        name,
        target_or_channel: str | grpc.Channel,
        /,
        metadata: list[tuple] = [],
        executor: ThreadPoolExecutor = None,
    ):
        """初始化JQuant客户端对象。

        Args:
            name(str): 客户端名称。
            target_or_channel(str | grpc.Channel): 目标地址或gRPC通道对象。如果是字符串，则将其作为目标地址进行初始化。
            metadata(list[tuple], 可选): 全局元数据列表，每次请求都会带上这个元数据, 作为后端识别该客户端的标识, 默认为空列表。
            executor (ThreadPoolExecutor, 可选): 线程池执行器。

        """

        self.name = name
        self._metadata = metadata + [("name", name), ("client", "jquant-python")]
        self._executor = (
            executor
            if executor
            else ThreadPoolExecutor(max_workers=64, thread_name_prefix="jquant-pc")
        )
        if isinstance(target_or_channel, str):
            self._channel = init_channel(target_or_channel)
        else:
            self._channel = target_or_channel
        self._stream = grpcpb.StreamServiceStub(self._channel)
        self._client = grpcpb.ExchangeServiceStub(self._channel)
        self._finished = threading.Event()

    def __str__(self):
        return f"{self.name}"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def close(self) -> None:
        self._finished.set()
        self._channel.close()

    def submit(self, fn, /, *args, **kwargs):
        """提交异步任务

        Args:
            fn (callable): 需要执行的函数
            *args: 位置参数
            **kwargs: 关键字参数
        """
        return self._executor.submit(fn, *args, **kwargs)

    def subscribe_instruments(
        self,
        platform: str,
        instruments: list[str],
        handler: Callable[[list[pb.Instrument]], None] = None,
    ) -> None | Generator[list[pb.Instrument], None, None]:
        """订阅标的信息

        Args:
            platform (str): 平台名称
            instruments (list[str]): 标的列表
            handler (Callable[[list[pb.Instrument]], 可选): 回调函数,如果没有回调函数,则返回生成器对象

        Yields:
            list[pb.Instrument]: 如果没有 handler 参数, 则返回标的信息列表

        """
        req = pb.GetInstrumentsRequest(
            platform=platform,
            instruments=instruments,
        )
        return self.subscribe(SubscribeMethod.INSTRUMENT, req, handler)

    def subscribe_tick(
        self,
        platforms: list[str],
        instruments: list[str],
        handler: Callable[[list[pb.Ticker]], None] = None,
        **kwargs,
    ) -> None | Generator[list[pb.Ticker], None, None]:
        """订阅行情

        Args:
            platforms (list[str]): 平台名称列表
            instruments (list[str]): 标的列表
            handler (Callable[[list[pb.Ticker]], None], 可选): 回调函数; 如果没有回调函数,则返回生成器对象
            **kwargs: 其他参数

        Yields:
            list[pb.Ticker]: 如果没有 handler 参数, 则返回行情信息列表
        """
        req = pb.GetTickersRequest(
            platforms=platforms,
            instruments=instruments,
            params=kwargs,
        )
        return self.subscribe(SubscribeMethod.TICKER, req, handler)

    def subscribe_kline(
        self,
        platform: str,
        instrument: str,
        period: str = "1m",
        handler: Callable[[list[pb.Kline]], None] = None,
        **kwargs,
    ) -> None | Generator[list[pb.Kline], None, None]:
        """订阅K线

        Args:
            platform (str): 平台名称
            instrument (str): 标的名称
            period (str): K线周期
            handler (Callable[[list[pb.Kline]], None], 可选): 回调函数; 如果没有回调函数,则返回生成器对象
            **kwargs: 其他参数

        Yields:
            list[pb.Kline]: 如果没有 handler 参数, 则返回K线信息列表
        """
        req = pb.GetKlineRequest(
            platform=platform,
            instrument=instrument,
            period=period,
            params=kwargs,
        )
        return self.subscribe(SubscribeMethod.KLINE, req, handler)

    def subscribe_order(
        self,
        platform: str,
        instruments: list[str],
        investor: str,
        strategy: str,
        handler: Callable[[list[pb.Order]], None] = None,
        **kwargs,
    ) -> None | Generator[list[pb.Order], None, None]:
        """订阅订单

        Args:
            platform (str): 平台名称
            instruments (list[str]): 标的列表
            investor (str): 投资者名称
            strategy (str): 策略名称
            handler (Callable[[list[pb.Order]], None], 可选): 回调函数; 如果没有回调函数,则返回生成器对象
            source (str, 可选): 订单来源, 和下单时的 source 对应
            tag (str, 可选): 订单标签, 和下单时的 tag 对应
            **kwargs: 其他参数

        Yields:
            list[pb.Order]: 如果没有 handler 参数, 则返回订单信息列表
        """
        req = pb.GetOrdersRequest(
            platform=platform,
            instruments=instruments,
            investor=investor,
            strategy=strategy,
            params=kwargs,
        )
        return self.subscribe(SubscribeMethod.ORDER, req, handler)

    def subscribe_config(
        self,
        platform: str,
        strategy: str,
        handler: Callable[[dict], None] = None,
        **kwargs,
    ) -> None | Generator[dict, None, None]:
        """订阅策略配置

        Args:
            platform (str): 平台名称
            strategy (str): 策略名称
            handler (Callable[[dict], None], 可选): 回调函数; 如果没有回调函数,则返回生成器对象
            **kwargs: 其他参数

        Yields:
            dict: 如果没有 handler 参数, 则返回策略配置信息
        """
        req = pb.GetConfigRequest(
            platform=platform,
            strategy=strategy,
            params=kwargs,
        )
        return self.subscribe(SubscribeMethod.CONFIG, req, handler)

    def ping(
        self,
        handler: Callable[[pb.Ticker], None] = None,
    ) -> None | Generator[list[pb.Ticker], None, None]:
        """订阅策略配置

        Args:
            platform (str): 平台名称
            strategy (str): 策略名称
            handler (Callable[[dict], None], 可选): 回调函数; 如果没有回调函数,则返回生成器对象
            **kwargs: 其他参数

        Yields:
            list[pb.Ticker]: 如果没有 handler 参数, 则返回 pong 信息
        """
        return self.subscribe(SubscribeMethod.PING, None, handler)

    def subscribe(
        self,
        method: SubscribeMethod,
        req: message.Message,
        handler: Callable[[Any], None] = None,
    ) -> None | Generator[Any, None, None]:
        """订阅数据流

        Args:
            method (str): 需要订阅的方法
            req (message.Message): 订阅的请求
            handler (Callable[[Any], None], 可选): 回调函数; 如果没有回调函数,则返回生成器对象

        Yields:
            Any: 如果没有传入回调函数, 则返回生成器对象; 否则调用回调函数

        Raises:
            ValueError: 未知的回复类型
        """

        iter = self.subscribe_iter(method, req)
        if handler:
            for result in iter:
                handler(result)
        else:
            return iter

    def subscribe_iter(
        self,
        method: SubscribeMethod,
        req: message.Message = None,
    ) -> Generator[Any, None, None]:
        """订阅数据流

        Args:
            method (str): 需要订阅的方法
            req (message.Message): 订阅的请求

        Yields:
            Any: 返回生成器对象

        Raises:
            ValueError: 未知的回复类型
        """
        sub = subscribe_request(method=method, req=req)
        log.info(f"[{sub.id}]>>>subscribe@{method.value}:{req}")

        # 作为前后端信号控制, 支持背压(Backpressure)模式
        def response_generator():
            q = queue.Queue()
            _next = lambda: q.put(sub)
            response_iterator = self._stream.Subscribe(
                request_generator(q), metadata=self._metadata
            )
            log.info("<<<waiting for stream response")

            return _next, response_iterator

        _next, response_iterator = response_generator()
        _next()

        # Receive responses
        while not self._finished.is_set():
            try:
                for response in response_iterator:
                    result: anypb.Any = response.result
                    if result.Is(pb.GetTickersReply.DESCRIPTOR):
                        reply = pb.GetTickersReply()
                        result.Unpack(reply)
                    elif result.Is(pb.GetOrdersReply.DESCRIPTOR):
                        reply = pb.GetOrdersReply()
                        result.Unpack(reply)
                    elif result.Is(pb.GetKlineReply.DESCRIPTOR):
                        reply = pb.GetKlineReply()
                        result.Unpack(reply)
                    elif result.Is(pb.GetConfigReply.DESCRIPTOR):
                        reply = pb.GetConfigReply()
                        result.Unpack(reply)
                    elif result.Is(pb.GetInstrumentsReply.DESCRIPTOR):
                        reply = pb.GetInstrumentsReply()
                        result.Unpack(reply)
                    else:
                        raise ValueError(f"unknown reply: {result}")

                    log.debug(f"[{response.id}]<<<{method.value}:{reply.result}")
                    # 避免处理回调函数时出现异常导致后续数据无法推送
                    try:
                        yield reply.result
                    except Exception as e:
                        log.error(
                            f"[{response.id}]handler error={e}, reply={reply.result}"
                        )

                    # 通知后端可以推送下一个信息
                    _next()
                    log.debug(f"[{sub.id}]>>>next@{method.value}:{req}")

            except grpc.RpcError as e:
                status_code = e.code()
                details = e.details()
                if status_code == grpc.StatusCode.UNAVAILABLE:
                    log.error(f"Service is unavailable: {details}")
                    # retry
                    time.sleep(1)
                    log.info(f"[{sub.id}]Retry to subscribe@{method.value}:{req}")
                    _next, response_iterator = response_generator()
                    _next()
                else:
                    raise e

    def get_ticker(self, platform: str, instrument: str, **kwargs) -> pb.Ticker:
        """获取指定平台和合约的行情信息。

        Args:
            platform (str): 平台名称
            instrument (str): 合约名称

        Returns:
            pb.Ticker: 行情信息的回复对象

        Raises:
            grpc.RpcError: gRPC调用错误
        """
        reply: pb.GetTickerReply = self._client.GetTicker(
            pb.GetTickerRequest(
                platform=platform,
                instrument=instrument,
                params=kwargs,
            ),
            metadata=self._metadata,
        )
        return reply.result

    def get_tickers(
        self,
        platforms: list[str],
        instruments: list[str],
        **kwargs,
    ) -> list[pb.Ticker]:
        """获取指定平台和证券的行情数据。

        Args:
            platforms (list[str]): 平台名称列表。
            instruments (list[str]): 标的列表。

        Returns:
            list[pb.Ticker]: 包含行情数据的响应。

        Raises:
            grpc.RpcError: gRPC调用错误
        """
        reply: pb.GetTickersReply = self._client.GetTickers(
            pb.GetTickersRequest(
                platforms=platforms,
                instruments=instruments,
                params=kwargs,
            ),
            metadata=self._metadata,
        )
        return reply.result

    def get_kline(
        self,
        platform: str,
        instrument: str,
        period: str,
        start_timestamp: int = 0,
        end_timestamp: int = 0,
        offset: int = 0,
        limit: int = 100,
        **kwargs,
    ) -> list[pb.Kline]:
        """
        获取K线数据。

        Args:
            platform (str): 平台名称
            instrument (str): 合约名称
            period (str): K线周期, 取值范围为 ["1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
            start_timestamp (int, 可选): 开始时间戳(毫秒)
            end_timestamp (int, 可选): 结束时间戳(毫秒)
            offset (int, 可选): 偏移量(默认为0)
            limit (int, 可选): 限制返回的数量(默认为100)

        Returns:
            list[pb.Kline]: K线数据回复对象

        Raises:
            grpc.RpcError: gRPC调用错误
        """
        reply: pb.GetKlineReply = self._client.GetKline(
            pb.GetKlineRequest(
                platform=platform,
                instrument=instrument,
                period=period,
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
                offset=offset,
                limit=limit,
                params=kwargs,
            ),
            metadata=self._metadata,
        )
        return reply.result

    def cancel(
        self,
        platform: str,
        instrument: str,
        client_order_ids: list[str],
        **kwargs,
    ) -> list[str]:
        """取消指定的订单

        Args:
            platform (str): 平台
            instrument (str): 标的
            client_order_id (list[str]): 下单后返回的 client_order_id

        Returns:
            list[str]: 返回正常取消的 client_order_id 列表

        Raises:
            grpc.RpcError: gRPC调用错误
        """
        reply: pb.CancelReply = self._client.Cancel(
            pb.CancelRequest(
                platform=platform,
                instrument=instrument,
                client_order_ids=client_order_ids,
                params=kwargs,
            ),
            metadata=self._metadata,
        )
        return reply.client_order_ids

    def buy(
        self,
        platform: str,
        instrument: str,
        price: str,
        amount: str,
        investor: str,
        strategy: str,
        source: str = None,
        tag: str = None,
        **kwargs,
    ) -> pb.Order:
        """执行买入操作。

        Args:
            platform (str): 交易平台名称。
            instrument (str): 交易工具名称。
            price (str): 买入价格。
            amount (str): 买入数量。
            investor (str): 投资者名称。
            strategy (str): 交易策略名称。
            source (str, 可选): 交易来源。
            tag (str, 可选): 交易标签。
            **kwargs: 其他可选参数。

        Returns:
            pb.Order: 买入操作的回复。

        Raises:
            grpc.RpcError: gRPC调用错误
        """
        reply: pb.BuyReply = self._client.Buy(
            pb.BuyRequest(
                platform=platform,
                instrument=instrument,
                price=price,
                amount=amount,
                investor=investor,
                strategy=strategy,
                source=source,
                tag=tag,
                params=kwargs,
            ),
            metadata=self._metadata,
        )
        return reply.result

    def sell(
        self,
        platform: str,
        instrument: str,
        price: str,
        amount: str,
        investor: str,
        strategy: str,
        source: str = None,
        tag: str = None,
        **kwargs,
    ) -> pb.Order:
        """执行卖出操作。
        Args:
            platform (str): 交易平台名称。
            instrument (str): 交易工具名称。
            price (str): 卖出价格。
            amount (str): 卖出数量。
            investor (str): 投资者名称。
            strategy (str): 交易策略名称。
            source (str, 可选): 交易来源。
            tag (str, 可选): 交易标签。
            **kwargs: 其他可选参数。

        Returns:
            pb.Order: 卖出操作的回复。

        Raises:
            grpc.RpcError: gRPC调用错误
        """

        reply: pb.SellReply = self._client.Sell(
            pb.SellRequest(
                platform=platform,
                instrument=instrument,
                price=price,
                amount=amount,
                investor=investor,
                strategy=strategy,
                source=source,
                tag=tag,
                params=kwargs,
            ),
            metadata=self._metadata,
        )
        return reply.result

    def close_buy(
        self,
        platform: str,
        instrument: str,
        price: str,
        amount: str,
        investor: str,
        strategy: str,
        source: str = None,
        tag: str = None,
        **kwargs,
    ) -> pb.Order:
        """执行平多操作。
        Args:
            platform (str): 交易平台名称。
            instrument (str): 交易工具名称。
            price (str): 卖出价格。
            amount (str): 卖出数量。
            investor (str): 投资者名称。
            strategy (str): 交易策略名称。
            source (str, 可选): 交易来源。
            tag (str, 可选): 交易标签。
            **kwargs: 其他可选参数。

        Returns:
            pb.Order: 卖出操作的回复。

        Raises:
            grpc.RpcError: gRPC调用错误
        """

        reply: pb.CloseBuyReply = self._client.CloseBuy(
            pb.CloseBuyRequest(
                platform=platform,
                instrument=instrument,
                price=price,
                amount=amount,
                investor=investor,
                strategy=strategy,
                source=source,
                tag=tag,
                params=kwargs,
            ),
            metadata=self._metadata,
        )
        return reply.result

    def close_sell(
        self,
        platform: str,
        instrument: str,
        price: str,
        amount: str,
        investor: str,
        strategy: str,
        source: str = None,
        tag: str = None,
        **kwargs,
    ) -> pb.Order:
        """执行平空单操作。

        Args:
            platform (str): 交易平台名称。
            instrument (str): 交易工具名称。
            price (str): 卖出价格。
            amount (str): 卖出数量。
            investor (str): 投资者名称。
            strategy (str): 交易策略名称。
            source (str, 可选): 交易来源。
            tag (str, 可选): 交易标签。
            **kwargs: 其他可选参数。
        Returns:
            pb.Order: 卖出操作的回复。

        Raises:
            grpc.RpcError: gRPC调用错误
        """
        reply: pb.CloseSellReply = self._client.CloseSell(
            pb.CloseSellRequest(
                platform=platform,
                instrument=instrument,
                price=price,
                amount=amount,
                investor=investor,
                strategy=strategy,
                source=source,
                tag=tag,
                params=kwargs,
            ),
            metadata=self._metadata,
        )
        return reply.result

    def get_order(
        self,
        platform: str,
        instrument: str,
        client_order_id: str,
        **kwargs,
    ) -> pb.Order:
        """获取订单

        Args:
            platform (str): 平台
            instrument (str): 标的
            client_order_id (str): 客户端订单编号

        Returns:
            pb.Order: 订单信息

        Raises:
            grpc.RpcError: gRPC调用错误
        """

        reply: pb.GetOrderReply = self._client.GetOrder(
            pb.GetOrderRequest(
                platform=platform,
                instrument=instrument,
                client_order_id=client_order_id,
                params=kwargs,
            ),
            metadata=self._metadata,
        )
        return reply.result

    def get_orders(
        self,
        platform: str,
        instruments: list[str],
        investor: str,
        strategy: str,
        client_order_ids: list[str] = [],
        status: str = "",
        start_timestamp: int = 0,
        end_timestamp: int = 0,
        offset: int = 0,
        limit: int = 100,
        **kwargs,
    ) -> list[pb.Order]:
        """获取订单列表

        Args:
            platform (str): 平台
            instrument (list[str]): 标的
            investor (str): 投资者编号
            strategy (str): 策略编号
            client_order_ids (list[str], 可选): 客户端订单编号
            status (str, 可选): 订单状态
            start_timestamp (int, 可选): 开始时间戳
            end_timestamp (int, 可选): 结束时间戳
            offset (int, 可选): 偏移量
            limit (int, 可选): 限制数量

        Returns:
            list[pb.Order]: 订单列表

        Raises:
            grpc.RpcError: gRPC调用错误
        """
        reply: pb.GetOrdersReply = self._client.GetOrders(
            pb.GetOrdersRequest(
                platform=platform,
                instruments=instruments,
                investor=investor,
                strategy=strategy,
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
                offset=offset,
                limit=limit,
                status=status,
                client_order_ids=client_order_ids,
                params=kwargs,
            ),
            metadata=self._metadata,
        )
        return reply.result

    def get_position(
        self,
        platform: str,
        investor: str = None,
        strategy: str = None,
        **kwargs,
    ) -> list[pb.Position]:
        """获取持仓

        Args:
            platform (str): 平台
            **kwargs: 其他参数

        Returns:
            list[pb.Position]: 持仓列表

        Raises:
            grpc.RpcError: gRPC调用错误
        """
        reply: pb.GetPositionReply = self._client.GetPosition(
            pb.GetPositionRequest(
                platform=platform,
                investor=investor,
                strategy=strategy,
                params=kwargs,
            ),
            metadata=self._metadata,
        )
        return reply.result

    def set_leverage(
        self,
        platform: str,
        instrument: str,
        leverage: int,
        **kwargs,
    ) -> int:
        """设置杠杆

        Args:
            platform (str): 平台
            instrument (str): 标的
            leverage (int): 杠杆倍数
            **kwargs: 其他参数

        Returns:
            leverage: 设置杠杆返回,包含设置杠杆的信息

        Raises:
            grpc.RpcError: gRPC调用错误
        """
        reply: pb.SetLeverageReply = self._client.SetLeverage(
            pb.SetLeverageRequest(
                platform=platform,
                instrument=instrument,
                leverage=leverage,
                params=kwargs,
            ),
            metadata=self._metadata,
        )
        return reply.leverage

    def get_instruments(
        self,
        platform: str,
        kinds: list[str],
        instruments: list[str] = [],
        **kwargs,
    ) -> list[pb.Instrument]:
        """获取合约列表

        Args:
            platform (str): 平台
            kinds (list[str]): 合约类型列表
            instruments (list[str], 可选): 合约列表
            **kwargs: 其他参数

        Returns:
            list[pb.Instrument]: 合约列表

        Raises:
            grpc.RpcError: gRPC调用错误
        """
        kvs = [kind.value for kind in kinds]
        reply: pb.GetInstrumentsReply = self._client.GetInstruments(
            pb.GetInstrumentsRequest(
                platform=platform,
                kinds=kvs,
                instruments=instruments,
                params=kwargs,
            ),
            metadata=self._metadata,
        )
        return reply.result

    def get_config(
        self,
        platform: str,
        strategy: str,
        **kwargs,
    ) -> dict:
        """获取策略配置

        Args:
            platform (str): 平台
            strategy (str): 策略代码
            **kwargs: 其他参数

        Returns:
            list[pb.Instrument]: 合约列表

        Raises:
            grpc.RpcError: gRPC调用错误
        """
        reply: pb.GetInstrumentsReply = self._client.GetConfig(
            pb.GetConfigRequest(
                platform=platform,
                strategy=strategy,
                params=kwargs,
            ),
            metadata=self._metadata,
        )
        return reply.result

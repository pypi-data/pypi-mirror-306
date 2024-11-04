# -*- coding: utf-8 -*-
import asyncio
import json
import traceback
import warnings
from functools import wraps
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Union,
    Tuple, cast
)
from urllib.parse import urlparse

import anyio
from broadcaster import Broadcast, BroadcastBackend
from fastapi_limiter import FastAPILimiter, ws_default_callback
from fastapi_limiter.depends import WebSocketRateLimiter
from redis.asyncio import Redis
from starlette._exception_handler import _lookup_exception_handler
from starlette._utils import is_async_callable
from starlette.concurrency import run_in_threadpool
from starlette.websockets import WebSocket
from typing_extensions import Annotated, Doc, Literal  # noqa

from fastapi_channels.exceptions import (
    WebSocketException,
    WebSocketExceptionHandler,
    PermissionDenied,
    ActionNotExist,
    ActionIsDeprecated)
from fastapi_channels.lifespan import ChannelLifespanEvent
from fastapi_channels.metaclssses import ActionConsumerMeta
from fastapi_channels.permission import BasePermission, AllowAny
from fastapi_channels.types import Lifespan, DecoratedCallable

DEFAULT_QUERY_TOKEN_KEY = 'token'
DEFAULT_COOKIE_TOKEN_KEY = 'token'
# DEFAULT_PERMISSION_CLASSES = ("fastapi_channels.permissions.AllowAny",)
DEFAULT_PERMISSION_CLASSES = (AllowAny,)


class FastAPIChannel:
    """
    为fastapi-channels全局注册类变量，在使用Channel的时候部分变量没有指定将会使用这个
    """
    broadcast: Optional[Broadcast] = None
    _new_broadcast: bool = False
    _new_limiter: bool = False
    # authentication
    query_token_key: Optional[str] = None
    cookie_token_key: Optional[str] = None
    permission_classes: Any = DEFAULT_PERMISSION_CLASSES
    # other
    # pagination_class: Any = None
    throttle_classes: Optional[WebSocketRateLimiter] = None

    @classmethod
    async def init(
            cls,
            url: Optional[str] = None,
            backend: Optional[BroadcastBackend] = None,
            broadcast: Optional[Broadcast] = None,
            # fastapi-limiter
            limiter_url: Optional[str] = None,
            redis=None,
            prefix: str = "fastapi-channel",
            identifier: Optional[Callable] = None,
            http_callback: Optional[Callable] = None,
            ws_callback: Callable = ws_default_callback,
            # TODO: 上面可能要删去
            # permission 权限
            permission_classes: Optional[Sequence[Union[BasePermission, str]]] = None,
            # throttling 限流器
            throttle_classes: Optional[WebSocketRateLimiter] = None,
            # pagination 分页器
            # pagination_class: Optional[Sequence] = None,
            # authentication
            query_token_key: Optional[str] = None,
            cookie_token_key: Optional[str] = None
    ):
        assert url is not None or limiter_url is not None or redis is not None, \
            "Either 'url' or 'limiter_url' or 'redis' must be provided."
        if url or limiter_url:
            url = url or limiter_url
            limiter_url = limiter_url or url
            parsed_url = urlparse(limiter_url)
            if parsed_url.scheme not in ("redis", "rediss"):
                raise ValueError('A valid Redis URL is required')
        if broadcast:
            cls.broadcast = broadcast
        else:
            cls.broadcast = Broadcast(url=url, backend=backend)
            cls._new_broadcast = True
        cls.permission_classes = permission_classes or cls.permission_classes
        cls.throttle_classes = throttle_classes or cls.throttle_classes
        # cls.pagination_class = pagination_class or cls.pagination_class
        if not FastAPILimiter.redis:
            limiter_redis = redis or await Redis.from_url(limiter_url)
            _fastapi_limiter_init_additional_key = {}
            if identifier: _fastapi_limiter_init_additional_key['identifier'] = identifier
            if http_callback: _fastapi_limiter_init_additional_key['http_callback'] = http_callback
            await FastAPILimiter.init(
                redis=limiter_redis,
                prefix=prefix,
                ws_callback=ws_callback,
                **_fastapi_limiter_init_additional_key
            )
            cls._new_limiter = True

        cls.query_token_key = query_token_key or DEFAULT_QUERY_TOKEN_KEY
        cls.cookie_token_key = cookie_token_key or DEFAULT_COOKIE_TOKEN_KEY
        await cls.broadcast.connect()

    @classmethod
    async def close(cls):
        if cls._new_broadcast:
            await cls.broadcast.disconnect()
        if cls._new_limiter:
            await FastAPILimiter.close()


class BaseChannel:
    """
    基础BaseChannel只实现:
        1. 房间构建
        2. 消息处理
        3. 事件：加入房间和退出房间
        4. 请求限速
        5. 基础的用户验证
        6. 错误返回
        7. 聊天记录的保存(*可选)(后续实现)
    """
    # # # - base room settings    - # # #
    # - base room connect settings    - #
    channel: str = 'default_channel'

    # - base room Can be instantiated settings    - #
    # room
    max_connection: Optional[int] = None
    # encoding: Optional[str] = None  # May be "text", "bytes", or "json".
    # 默认编码方式，对应直接调用encode和decode的处理方式
    on_join: Optional[Sequence[Callable[[], Any]]] = None
    on_leave: Optional[Sequence[Callable[[], Any]]] = None
    lifespan: Optional[Lifespan] = None
    # limiter
    history_key: str = f'history:{channel}'
    max_history: Optional[int] = None
    limiter_depends: Optional[List] = None
    # recent message
    timedelta: Optional[int] = None
    # permission
    permission_classes: Union[List, Tuple, Callable, BasePermission, None] = FastAPIChannel.permission_classes
    throttle_classes: Optional[WebSocketRateLimiter] = FastAPIChannel.throttle_classes

    def __init__(
            self,
            *,
            channel: Optional[str] = None,
            max_connection: Optional[int] = None,
            history_key: Optional[str] = None,
            max_history: Optional[int] = None,
            limiter_depends: Optional[List] = None,
            permission_classes: Optional[List] = None,
            throttle_classes: Optional[WebSocketRateLimiter] = None,
            on_join: Optional[Sequence[Callable[[], Any]]] = None,
            on_leave: Optional[Sequence[Callable[[], Any]]] = None,
            lifespan: Optional[Lifespan] = None,
    ):
        self._exc_handlers = {}
        assert lifespan is None or (
                on_join is None and on_leave is None
        ), "Use either 'lifespan' or 'on_join'/'on_leave', not both."
        self.permission_classes = permission_classes or self.permission_classes
        self.limiter_depends = limiter_depends or self.limiter_depends
        self.max_history = max_history or self.max_history
        self.history_key = history_key or self.history_key
        self.max_connection = max_connection or self.max_connection
        self.channel = channel or self.channel
        if not isinstance(self.permission_classes, List):
            if isinstance(self.permission_classes, Tuple):
                self.permission_classes = list(self.permission_classes)
            else:
                self.permission_classes = [self.permission_classes]
        self.event_manage = ChannelLifespanEvent(
            on_join=on_join or self.on_join, on_leave=on_leave or self.on_leave,
            lifespan=lifespan or self.lifespan)
        self.throttle_classes = throttle_classes or self.throttle_classes

    async def connect(self, websocket: WebSocket, channel: Optional[str] = None) -> None:
        channel = channel or self.channel
        await websocket.accept()
        self._exc_handlers, status_handlers = websocket.scope.get('starlette.exception_handlers')
        if self.max_connection is not None:
            await self.check_connection_count(channel)
        await self.check_permission_classes(websocket)
        await self._lifespan(websocket, channel)

    async def disconnect(self, websocket: WebSocket) -> None:
        await websocket.close()

    async def close(self, websocket: WebSocket) -> None:
        await websocket.close()

    @staticmethod
    async def broadcast_to_personal(websocket: WebSocket, message: Any) -> None:
        """
        @example:
            ```
            class AChannel(Channel):
                @action(name='open')
                async def open_action(self,websocket:Websocket,channel:str):
                    await self.broadcast_to_personal(websocket, 'Hello, Channel!')
            ```
            ```
            channel=Channel()

            @channel.action(name='open')
            async def open_action(self,websocket:Websocket,channel:str):
                await channel.broadcast_to_personal(websocket, 'Hello, Channel!')
            ```
        """
        await websocket.send_text(message)

    @staticmethod
    async def broadcast_to_channel(channel: str, message: Any) -> None:
        """
        @example:
            ```
            class AChannel(Channel):
                @action(name='open')
                async def open_action(self,websocket:Websocket,channel:str,data:dict):
                    await self.broadcast_to_channel(channel, 'Hello, Channel!')
            ```
            ```
            channel=Channel()

            @channel.action(name='open')
            async def open_action(self,websocket:Websocket,channel:str,data:dict):
                await channel.broadcast_to_channel(channel, 'Hello, Channel!')
            ```
        """
        await FastAPIChannel.broadcast.publish(channel=channel, message=message)

    @staticmethod
    async def send_error(error_msg: Any, close: bool = False) -> None:
        raise WebSocketException(error_msg=error_msg, close=close)

    async def _handle_exception(self, task, websocket: WebSocket, channel: str):
        try:
            await task
        except Exception as exc:
            handler = None
            if handler is None:
                handler = _lookup_exception_handler(self._exc_handlers, exc)
            if handler is None:
                raise exc
            handler = cast(WebSocketExceptionHandler, handler)
            if is_async_callable(handler):
                await handler(websocket, exc)
            else:
                await run_in_threadpool(handler, websocket, exc)

    async def _handle(self, type: str, message: Optional[str] = None, **kwargs):
        if type == 'lifespan.join.complete':
            return await self._connect(websocket=kwargs.get('websocket'), channel=kwargs.get('channel'))
        if type == 'lifespan.join.failed':
            pass
        if type == 'lifespan.leave.complete':
            pass
        if type == 'lifespan.leave.failed':
            pass

    async def _lifespan(self, websocket: WebSocket, channel: str) -> None:
        """
        Handle fastapi-channels channel lifespan messages, which allows us to manage application
        join and leave events.
        """
        joined = False  # 是否执行join函数
        kwargs = {
            'websocket': websocket,
            'channel': channel,
        }
        # 默认如果是中间部分错误的话，结束不会被运行，除非你捕获了lifespan中的异常并使用finally的语句指定代码
        try:
            async with self.event_manage.lifespan_context(websocket, channel):
                joined = True
                await self._handle(type="lifespan.join.complete", **kwargs)
        except BaseException:
            exc_text = traceback.format_exc()
            if joined:
                await self._handle(type="lifespan.leave.failed", message=exc_text, **kwargs)
            else:
                await self._handle(type="lifespan.join.failed", message=exc_text, **kwargs)
            raise
        else:
            await self._handle(type="lifespan.leave.complete", **kwargs)

    async def _connect(self, websocket: WebSocket, channel: str) -> None:
        async with anyio.create_task_group() as task_group:
            # run until first is complete
            async def run_chatroom_ws_receiver() -> None:
                try:
                    await self._receiver(websocket=websocket, channel=channel)
                except RuntimeError:  # 客户端直接断开连接诱发的异常(websocket.accept() first)
                    pass
                task_group.cancel_scope.cancel()

            task_group.start_soon(run_chatroom_ws_receiver)
            await self._sender(websocket=websocket, channel=channel)

    async def _receiver(self, websocket: WebSocket, channel: str):
        """接收信息"""
        async for message in websocket.iter_text():
            # Channel重写此处
            async def _task():
                if self.throttle_classes is not None: await self.throttle_classes(websocket, channel)
                await FastAPIChannel.broadcast.publish(channel=channel, message=message)

            await self._handle_exception(_task(), websocket, channel)

    async def _sender(self, websocket: WebSocket, channel: str):
        """发送信息"""
        async with FastAPIChannel.broadcast.subscribe(channel=channel) as subscriber:
            async for event in subscriber:
                await websocket.send_text(event.message)

    async def get_permissions(self, action: Optional[str] = None, **kwargs) -> List:
        """
        获取需要验证的权限列表
        Args:
            action: 对应的action
            **kwargs:

        Returns:

        """
        if action:
            # BaseChannel不对action做处理，你应该使用Channel类
            warnings.warn("BaseChannel class does not handle actions,You should use the Channel class.")
        return self.permission_classes

    async def check_permission_classes(self, websocket: WebSocket) -> None:
        """只检查permission_classes的权限认证"""
        for permission in self.permission_classes:
            if await self._check_permission(
                    websocket=websocket,
                    action=None,
                    permission=permission
            ) is False:
                raise PermissionDenied(close=True)

    @staticmethod
    async def _check_permission(websocket: WebSocket, action: Optional[str], permission: Any, **kwargs) -> bool:
        if permission is None:
            return True
        elif isinstance(permission, type) and issubclass(permission, BasePermission):
            return await permission().has_permission(websocket=websocket, action=action, **kwargs)
        elif callable(permission):
            if asyncio.iscoroutinefunction(permission):
                return await permission(websocket, action, permission, **kwargs)
            return permission(websocket, action, permission, **kwargs)
        return False

    async def get_connection_count(self, channel: str) -> int:  # noqa
        """
        获取当前房间连接的人数
        """
        return len(FastAPIChannel.broadcast._subscribers.get(channel, set()))  # type: ignore

    async def check_connection_count(self, channel: str) -> int:
        """
        如果当前人数大于房间设置的上限人数就退出，否则返回当前房间人数
        """
        current_conn_nums = await self.get_connection_count(channel)
        if self.max_connection is None or current_conn_nums < self.max_connection:
            return current_conn_nums
        await self.send_error(
            error_msg='The current number of channel connections is greater than the maximum number of connections',
            close=True
        )

    @staticmethod
    async def encode_json(data: dict) -> str:
        return json.dumps(data, ensure_ascii=False)

    @staticmethod
    async def decode_json(message: str) -> dict:
        return json.loads(message)

    async def encode(self, data: Any):
        return await self.encode_json(data)

    async def decode(self, message: Any) -> dict:
        return await self.decode_json(message)

    def on_event(self, event_type: str) -> DecoratedCallable:  # 装饰器
        return self.event_manage.on_event(event_type)

    def add_event_handler(self, event_type: str, func: Callable, ) -> None:  # pragma: no cover
        self.event_manage.add_event_handler(event_type, func)


class Channel(BaseChannel, metaclass=ActionConsumerMeta):
    """
    Channel在 BaseChannel 的基础上又实现:
        1. 通过action装饰器解析处理用户发送的数据包,同时可以在原有的权限基础上进行权限认证
        2. 通过limiter装饰器(需要先注册action装饰器),可对单个类型的action进行限流
    """

    def __init__(self, *, channel: Optional[str] = None, max_connection: Optional[int] = None,
                 history_key: Optional[str] = None, max_history: Optional[int] = None,
                 limiter_depends: Optional[List] = None, permission_classes: Optional[List] = None,
                 throttle_classes: Optional[WebSocketRateLimiter] = None,
                 on_join: Optional[Sequence[Callable[[], Any]]] = None,
                 on_leave: Optional[Sequence[Callable[[], Any]]] = None,
                 lifespan: Optional[Lifespan] = None):
        super().__init__(
            channel=channel, max_connection=max_connection, history_key=history_key,
            max_history=max_history, limiter_depends=limiter_depends,
            permission_classes=permission_classes, throttle_classes=throttle_classes, on_join=on_join,
            on_leave=on_leave, lifespan=lifespan)

        if not hasattr(self, '_actions'):
            self._actions: Dict[str, tuple] = {}

    async def _receiver(self, websocket: WebSocket, channel: str):
        """接收信息"""
        async for message in websocket.iter_text():
            # Channel重写此处
            async def _task():
                if self.throttle_classes is not None: await self.throttle_classes(websocket, channel)
                # data: dict = json.loads(message)
                data: dict = await self.decode(message)
                await self.handle_action(
                    action=data.get('action', None),
                    request_id=int(data.get('request_id', 1)),
                    data=data,
                    websocket=websocket,
                    channel=channel
                ),

            await self._handle_exception(
                _task(),
                websocket=websocket,
                channel=channel
            )

    @property
    def actions(self) -> List[str]:
        return list(self._actions.keys())

    async def handle_action(
            self, websocket: WebSocket, channel: str,
            action: str, request_id: int, data: dict, **kwargs
    ) -> None:
        if action not in self.actions:
            raise ActionNotExist(request_id=request_id, close=False)
        await self.check_permissions(websocket=websocket, action=action, **kwargs)
        action_func_or_str, _ = self._actions[action]
        if isinstance(action_func_or_str, str):
            await getattr(self, action_func_or_str)(websocket=websocket, channel=channel, data=data)
        else:
            await action_func_or_str.call(websocket=websocket, channel=channel, data=data)

    def action(
            self,
            name: Optional[str] = None,
            permission: Optional[Any] = None,
            detached: bool = False,
            deprecated: bool = False,
    ) -> DecoratedCallable:
        if detached:
            raise NotImplementedError(
                'Sorry, the detached function has not been implemented yet and is currently only used for placeholder')

        def decorator(func):
            _name = name if name else func.__name__
            func.action = (_name, func.__doc__)
            perm_desc = 'Allow Anyone'
            if isinstance(permission, type) and issubclass(permission, BasePermission):
                perm_desc = permission.__doc__ or permission.has_permission.__doc__
            elif callable(permission):
                perm_desc = permission.__doc__
            elif isinstance(permission, bool):
                if not permission:
                    perm_desc = 'Not Allow Anyone'
            func.permission = (permission, perm_desc)

            @wraps(func)
            async def wrapper(*args, **kwargs):
                if deprecated:
                    raise ActionIsDeprecated(error_msg=f"The function '{_name}' is deprecated.")
                return await func(*args, **kwargs)

            wrapper.action = func.action
            wrapper.call = wrapper
            self._actions[_name] = (wrapper, permission)
            return wrapper

        return decorator

    async def get_permissions(self, action: Optional[str] = None, **kwargs) -> List:
        """
        获取需要验证的权限列表
        Args:
            action: 对应的action
            **kwargs:

        Returns:

        """
        _, perm_call = self._actions.get(action, None)
        if perm_call is not None:
            if not isinstance(perm_call, List):
                if isinstance(perm_call, Tuple):
                    perm_call = list(perm_call)
                else:
                    perm_call = [perm_call]
            return self.permission_classes + perm_call
        return self.permission_classes

    async def check_permissions(self, websocket: WebSocket, action: str = None, **kwargs) -> None:
        """检查permission_classes的权限认证和对应action的权限认证"""
        for permission in await self.get_permissions(action=action):
            if await self._check_permission(
                    websocket=websocket, action=action, permission=permission, **kwargs
            ) is False:
                raise PermissionDenied(close=False)

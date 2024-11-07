import asyncio
from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import partial
from typing import Any, AsyncIterator, Callable, Coroutine, Protocol, Self, Sequence, final


__all__ = [
    'T_CONTROLLER',
    'wait_gather',
    'wait_stack',
    'wait_fixed',
    'wait_compensation',
    'run_after',
    'run_before',
    'T_CORO_FACTORY',
    'scheduled',
    'schedule'
]


class T_CONTROLLER(Protocol):
    @asynccontextmanager # type: ignore
    async def wrap_loop(self: Self) -> AsyncIterator[None]:
        ...

    @asynccontextmanager # type: ignore
    async def wrap_call(self: Self) -> AsyncIterator[None]:
        ...

    def __and__(self: Self, other: 'T_CONTROLLER') -> 'wait_stack':
        if isinstance(self, wait_stack) and isinstance(other, wait_stack):
            return wait_stack([*self.controllers, *other.controllers])
        elif isinstance(self, wait_stack):
            return wait_stack([*self.controllers, other])
        elif isinstance(other, wait_stack):
            return wait_stack([self, *other.controllers])
        else:
            return wait_stack([self, other])

    def __or__(self: Self, other: 'T_CONTROLLER') -> 'wait_gather':
        if isinstance(self, wait_gather) and isinstance(other, wait_gather):
            return wait_gather([*self.controllers, *other.controllers])
        elif isinstance(self, wait_gather):
            return wait_gather([*self.controllers, other])
        elif isinstance(other, wait_gather):
            return wait_gather([self, *other.controllers])
        else:
            return wait_gather([self, other])


@final
@dataclass(slots=True)
class wait_gather(T_CONTROLLER):
    controllers: Sequence[T_CONTROLLER] = field(default_factory=list)

    @asynccontextmanager
    async def wrap_loop(self: Self) -> AsyncIterator[None]:
        async with AsyncExitStack() as stack:
            await asyncio.gather(*[
                stack.enter_async_context(controller.wrap_loop())
                for controller in self.controllers
            ])
            yield

    @asynccontextmanager
    async def wrap_call(self: Self) -> AsyncIterator[None]:
        async with AsyncExitStack() as stack:
            await asyncio.gather(*[
                stack.enter_async_context(controller.wrap_call())
                for controller in self.controllers
            ])
            yield


@final
@dataclass(slots=True)
class wait_stack(T_CONTROLLER):
    controllers: Sequence[T_CONTROLLER] = field(default_factory=list)

    @asynccontextmanager
    async def wrap_loop(self: Self) -> AsyncIterator[None]:
        async with AsyncExitStack() as stack:
            for controller in self.controllers:
                await stack.enter_async_context(controller.wrap_loop())
            yield

    @asynccontextmanager
    async def wrap_call(self: Self) -> AsyncIterator[None]:
        async with AsyncExitStack() as stack:
            for controller in self.controllers:
                await stack.enter_async_context(controller.wrap_call())
            yield


@final
@dataclass(slots=True)
class wait_fixed(T_CONTROLLER):
    delay: timedelta = field(default=timedelta(seconds=60))

    @asynccontextmanager
    async def wrap_loop(self: Self) -> AsyncIterator[None]:
        yield

    @asynccontextmanager
    async def wrap_call(self: Self) -> AsyncIterator[None]:
        await asyncio.sleep(self.delay.total_seconds())
        print(f'{type(self).__qualname__}.wail({self.delay.total_seconds()})')
        yield


@final
@dataclass(slots=True)
class wait_compensation(T_CONTROLLER):
    delay: timedelta = field(default=timedelta(seconds=60))
    start: datetime = field(init=False)
    calls: int = field(init=False, default=0)
    compensation: timedelta = field(init=False, default=timedelta(seconds=0))

    @asynccontextmanager
    async def wrap_loop(self: Self) -> AsyncIterator[None]:
        self.start = datetime.now()
        yield

    @asynccontextmanager
    async def wrap_call(self: Self) -> AsyncIterator[None]:
        next_call = self.start + self.delay * (self.calls + 1)
        wait = (next_call - datetime.now()).total_seconds()
        await asyncio.sleep(wait)
        yield
        self.calls += 1


@final
@dataclass(slots=True)
class run_after(T_CONTROLLER):
    after: datetime | timedelta = field()

    @asynccontextmanager
    async def wrap_loop(self: Self) -> AsyncIterator[None]:
        if isinstance(self.after, timedelta):
            self.after = datetime.now() + self.after
            wait = self.after - datetime.now()
        else:
            wait = self.after - datetime.now(self.after.tzinfo)
        await asyncio.sleep(wait.total_seconds())
        yield

    @asynccontextmanager
    async def wrap_call(self: Self) -> AsyncIterator[None]:
        yield


@final
@dataclass(slots=True)
class run_before(T_CONTROLLER):
    before: datetime | timedelta = field()

    @asynccontextmanager
    async def wrap_loop(self: Self) -> AsyncIterator[None]:
        if isinstance(self.before, timedelta):
            self.before = datetime.now() + self.before
        yield

    @asynccontextmanager
    async def wrap_call(self: Self) -> AsyncIterator[None]:
        assert isinstance(self.before, datetime)
        if datetime.now(self.before.tzinfo) > self.before:
            raise StopIteration()
        yield


T_CORO_FACTORY = Callable[[], Coroutine[Any, Any, Any]]


@final
@dataclass(slots=True)
class scheduled:
    coro_factory: T_CORO_FACTORY = field()
    controller: T_CONTROLLER = field(kw_only=True)
    loop: asyncio.AbstractEventLoop = field(kw_only=True)
    job: asyncio.Task = field(init=False)

    @classmethod
    def schedule(
        cls: type[Self],
        controller: T_CONTROLLER,
        *,
        loop: asyncio.AbstractEventLoop,
    ) -> Callable[[T_CORO_FACTORY], Self]:
        if callable(loop):
            loop = loop()

        return partial(
            cls,
            controller=controller,
            loop=loop,
        )

    def __post_init__(self: Self, /) -> None:
        self.job = self.loop.create_task(self())

    async def __call__(self: Self, /) -> None:
        async with self.controller.wrap_loop():
            while True:
                async with self.controller.wrap_call():
                    await self.coro_factory()


schedule = scheduled.schedule


if __name__ == '__main__':
    '''Example'''
    asyncio.set_event_loop(loop := asyncio.new_event_loop())

    start_create = datetime.now()
    last_execute = None
    @schedule(((run_after(timedelta(seconds=5)) | run_before(timedelta(seconds=15))) & wait_compensation(timedelta(seconds=1))), loop=loop)
    async def foo():
        global last_execute
        periodicity = datetime.now() - (last_execute or datetime.now())
        after_create = datetime.now() - start_create
        print(f'{type(foo).__qualname__}() -> ok ; after_create=[{after_create}] ; last_execute=[{last_execute}] ; periodicity=[{periodicity}]')
        last_execute = datetime.now()


    loop.run_forever()

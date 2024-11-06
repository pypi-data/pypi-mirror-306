import asyncio
from collections.abc import AsyncIterator, Awaitable, Sequence
from typing import Any, Callable, Generic, Optional, TypeVar, Union

from reactivex import Observable, abc, from_iterable
from reactivex import from_future as rx_from_future
from reactivex.disposable import Disposable

T = TypeVar("T")
TSource = TypeVar("TSource")
TResult = TypeVar("TResult")


class HybridObservable(Observable[T], Generic[T]):
    def __init__(self, observable: Observable[T]):
        super().__init__(observable._subscribe)
        self._observable: Observable[T] = observable

    def run(self) -> T:
        return self._observable.run()

    def pipe(self, *operators: Callable[[Observable[Any]], Observable[Any]]) -> "HybridObservable[T]":  # type: ignore
        return HybridObservable(self._observable.pipe(*operators))

    def subscribe(
        self,
        on_next: abc.ObserverBase[T] | Callable[[T], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
        on_completed: Callable[[], None] | None = None,
        *,
        scheduler: abc.SchedulerBase | None = None,
    ) -> abc.DisposableBase:
        return self._observable.subscribe(on_next, on_error, on_completed, scheduler=scheduler)

    async def arun(self) -> T:
        future: asyncio.Future[T] = asyncio.Future()
        last_value: Optional[T] = None
        error_occurred = False

        def on_next(value: T) -> None:
            nonlocal last_value
            last_value = value

        def on_error(error: Exception) -> None:
            nonlocal error_occurred
            error_occurred = True
            if not future.done():
                future.set_exception(error)

        def on_completed() -> None:
            if not future.done():
                if error_occurred:
                    return
                if last_value is not None:
                    future.set_result(last_value)
                else:
                    future.set_exception(
                        asyncio.InvalidStateError("Observable completed without emitting a value")
                    )

        disposable = self.subscribe(on_next, on_error, on_completed)

        try:
            return await future
        finally:
            disposable.dispose()

    async def apipe(
        self, *operators: Callable[[Observable[Any]], Observable[Any]]
    ) -> "HybridObservable[Any]":
        """
        Asynchronous version of pipe.
        """
        return HybridObservable(self._observable.pipe(*operators))

    async def asubscribe(
        self,
        on_next: Optional[Callable[[T], Awaitable[Any]]] = None,
        on_error: Optional[Callable[[Exception], Awaitable[Any]]] = None,
        on_completed: Optional[Callable[[], Awaitable[Any]]] = None,
    ) -> Disposable:
        """
        Subscribe asynchronously to the observable sequence.
        """
        future: asyncio.Future[None] = asyncio.Future()

        async def async_on_next(value: T) -> None:
            if on_next:
                await on_next(value)

        async def async_on_error(error: Exception) -> None:
            if on_error:
                await on_error(error)
            if not future.done():
                future.set_exception(error)

        async def async_on_completed() -> None:
            if on_completed:
                await on_completed()
            if not future.done():
                future.set_result(None)

        disposable = self.subscribe(
            lambda x: asyncio.create_task(async_on_next(x)) and None,
            lambda e: asyncio.create_task(async_on_error(e)) and None,
            lambda: asyncio.create_task(async_on_completed()) and None,
        )

        def cancel_subscription() -> None:
            disposable.dispose()
            if not future.done():
                future.cancel()

        return Disposable(cancel_subscription)

    async def __aiter__(self) -> "AsyncIterator[T]":
        queue: asyncio.Queue[Union[T, Exception]] = asyncio.Queue()
        done = asyncio.Event()
        subscription: Optional[abc.DisposableBase] = None

        def on_next(value: T) -> None:
            queue.put_nowait(value)

        def on_completed() -> None:
            done.set()

        def on_error(error: Exception) -> None:
            if not done.is_set():
                queue.put_nowait(error)
                done.set()

        subscription = self.subscribe(on_next, on_error, on_completed)

        try:
            while not done.is_set() or not queue.empty():
                try:
                    item = await queue.get()
                    if isinstance(item, Exception):
                        raise item
                    yield item
                except asyncio.CancelledError:
                    break
        finally:
            if subscription:
                subscription.dispose()

    @classmethod
    def from_iterable(
        cls: type["HybridObservable[TSource]"],
        iterable: Union[list[TSource], tuple[TSource, ...], set[TSource]],
    ) -> "HybridObservable[TSource]":
        return cls(from_iterable(iterable))

    @classmethod
    async def from_async_iterable(
        cls: type["HybridObservable[TSource]"], async_iterable: AsyncIterator[TSource]
    ) -> "HybridObservable[TSource]":
        async def to_list(ait: AsyncIterator[TSource]) -> Sequence[TSource]:
            return [item async for item in ait]

        items = await to_list(async_iterable)
        return cls(from_iterable(items))

    @classmethod
    def from_future(
        cls: type["HybridObservable[TSource]"], future: asyncio.Future[TSource]
    ) -> "HybridObservable[TSource]":
        return cls(rx_from_future(future))

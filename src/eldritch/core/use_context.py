from __future__ import annotations

from abc import ABCMeta
from inspect import stack
from typing import Any, ClassVar, Dict, Type, cast

from eldritch.core.context import EldritchContext


class UseContext:
    """This class is a mixin which guarantees context accessability."""

    class ContextNotFound(RuntimeError):
        """This exception is raised when context is not found within call stack."""

    ctx: EldritchContext

    def __init__(self) -> None:
        self.ctx = self.find_context()

    def __post_init__(self) -> None:
        pass

    @staticmethod
    def find_context(*, skip: int = 2) -> EldritchContext:
        """Find EldritchContext in call stack.

        Parameters
        ----------
        skip : int, optional
            First levels of stack to skip, by default 2

        """
        call_stack = stack(context=0)[skip:]

        for frame in call_stack:
            ctx = frame.frame.f_locals.get("ctx", None)

            if isinstance(ctx, EldritchContext):
                return ctx

            frame_self = frame.frame.f_locals.get("self", None)
            if isinstance(frame_self, EldritchContext):
                return frame_self

            ctx = getattr(frame_self, "ctx", None)

            if isinstance(ctx, EldritchContext):
                return ctx

        raise UseContext.ContextNotFound("Context not found in call stack.")


class _UseContextOnceMeta(ABCMeta):

    __instances__: Dict[EldritchContext, _UseContextOnceMeta]

    def __new__(
        cls: Type[_UseContextOnceMeta],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> _UseContextOnceMeta:
        # Set placeholder for singleton instance, otherwise can not be assigned
        namespace["__instances__"] = {}
        # Instantiate class object
        new_class = super().__new__(cls, name, bases, namespace, **kwargs)
        # Ensure instance container was correctly set
        assert hasattr(new_class, "__instances__")
        return new_class

    def __call__(
        cls: _UseContextOnceMeta,
        *args: Any,
        **kwds: Any,
    ) -> _UseContextOnceMeta:

        ctx = UseContext.find_context(skip=2)

        # Instantiate class only when instance was not created already
        if ctx in cls.__instances__:
            return cls.__instances__[ctx]

        instance = super().__call__(*args, **kwds)
        cls.__instances__[ctx] = instance

        return cast(_UseContextOnceMeta, instance)


class UseContextOnce(UseContext, metaclass=_UseContextOnceMeta):
    """This class is a mixin which guarantees context accessability and makes class
    behave partially as singleton.

    Class is instantiated only one per context. On every consecutive attempt to
    instantiate it with already used context, same instance is returned.

    """

    __instances__: ClassVar[Dict[EldritchContext, _UseContextOnceMeta]]

"""This module groups project script override loaders."""

from __future__ import annotations

from typing import Type, cast

from eldritch import context


def get_context_class() -> Type[context.Context]:
    """Returns context class which have to be used for template rendering.

    Returns
    -------
    Type[context.Context]
        Context class or subclass.

    """
    try:
        from project.context import Context  # pylint: disable=import-outside-toplevel

        ctx = Context

    except ImportError:
        ctx = context.Context

    assert issubclass(ctx, context.Context)
    return cast(Type[context.Context], ctx)

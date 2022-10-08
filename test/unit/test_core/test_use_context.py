from __future__ import annotations

from typing import Callable

from eldritch.core.context import EldritchContext
from eldritch.core.use_context import UseContext, UseContextOnce


class TestUseContext:
    def test_find_context_just_above(self, ctx: EldritchContext) -> None:

        context = UseContext.find_context()

        assert isinstance(context, EldritchContext)
        assert context is ctx

    def test_find_context_just_above_in_class(self, ctx: EldritchContext) -> None:
        setattr(self, "ctx", ctx)
        del ctx

        context = UseContext.find_context()

        assert isinstance(context, EldritchContext)
        assert context is getattr(self, "ctx")

    def test_use_context_inheritance(self, ctx: EldritchContext) -> None:

        called = False

        class TestExample(UseContext):
            def test_f(self) -> None:
                nonlocal called

                assert isinstance(self.ctx, EldritchContext)
                assert self.ctx is ctx

                called = True

        def contextless() -> None:
            TestExample().test_f()

        contextless()

        assert called is True

    def _create_test_f(self) -> Callable[..., EldritchContext]:
        def test_f2() -> EldritchContext:
            ctx = UseContext.find_context()
            return ctx

        return test_f2

    def test_use_context_nested_function_call(self, ctx: EldritchContext) -> None:
        test_f2 = self._create_test_f()

        def test_f1() -> EldritchContext:
            return test_f2()

        found_ctx = test_f1()

        assert isinstance(found_ctx, EldritchContext)
        assert ctx is found_ctx


class TestUseContextOnce:
    def test_single_instance_per_ctx(self, ctx: EldritchContext) -> None:
        class TestExample(UseContextOnce):
            pass

        instance1 = TestExample()
        assert ctx is instance1.ctx

        instance2 = TestExample()
        assert ctx is instance2.ctx

        assert instance1 is instance2

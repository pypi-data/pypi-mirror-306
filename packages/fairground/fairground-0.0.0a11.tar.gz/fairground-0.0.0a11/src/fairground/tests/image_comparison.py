"""Wrapper for matplotlib's image comparison test decorator."""

import contextlib
import locale as locale_module
from collections.abc import Callable, Generator, Iterable
from typing import overload
from unittest import mock

import matplotlib as mpl
import matplotlib.testing.decorators


def _set_font_settings_for_testing() -> contextlib.AbstractContextManager[object]:
    return mock.patch.dict(
        mpl.rcParams,
        {
            "font.family": "DejaVu Sans",
            "text.hinting": "none",
            "text.hinting_factor": 8,
        },
    )


def _set_reproducibility_for_testing() -> contextlib.AbstractContextManager[object]:
    return mock.patch.dict(mpl.rcParams, {"svg.hashsalt": "matplotlib"})


@contextlib.contextmanager
def _setlocale(category: int, locale: str | Iterable[str | None] | None = None) -> Generator[str]:
    prev = locale_module.setlocale(category)
    v = locale_module.setlocale(category, locale)
    try:
        yield v
    finally:
        locale_module.setlocale(category, prev)


@contextlib.contextmanager
def _mpl_use(backend: str, *, force: bool = False) -> Generator[None]:
    orig = mpl.get_backend()
    mpl.use(backend, force=force)
    try:
        yield
    finally:
        mpl.use(orig, force=True)


@contextlib.contextmanager
def _matplotlib_testing_setup() -> Generator[None]:
    # copied from
    # https://github.com/matplotlib/matplotlib/blob/ed8131be7727f3e9454f1b30e14ed195ee2ada33/lib/matplotlib/testing/__init__.py#L18-L50
    # modified to support restoring settings

    # The baseline images are created in this locale, so we should use
    # it during all of the tests.

    with contextlib.ExitStack() as stack:
        try:
            stack.enter_context(_setlocale(locale_module.LC_ALL, "en_US.UTF-8"))
        except locale_module.Error:  # pragma: no cover
            try:
                stack.enter_context(_setlocale(locale_module.LC_ALL, "English_United States.1252"))
            except locale_module.Error as e:
                msg = (
                    "Could not set locale to English/United States. "
                    "Some date-related tests may fail."
                )
                raise RuntimeError(msg) from e

        with (
            _mpl_use("Agg"),
            # These settings *must* be hardcoded for running the comparison tests and
            # are not necessarily the default values as specified in rcsetup.py.
            _set_font_settings_for_testing(),
            _set_reproducibility_for_testing(),
        ):
            yield


@overload
def image_comparison[**P, R](f: Callable[P, R], /) -> Callable[P, R]: ...


@overload
def image_comparison[**P, R](*, tolerance: float) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def image_comparison[**P, R](
    f: Callable[P, R] | None = None,
    /,
    *,
    tolerance: float = 0,
) -> Callable[[Callable[P, R]], Callable[P, R]] | Callable[P, R]:
    """Return a custom decorator for image_comparison from matplotlib testing."""

    def _decorator(f: Callable[P, R]) -> Callable[P, R]:
        baseline_images = [f.__name__.removeprefix("test_")]
        return _matplotlib_testing_setup()(
            matplotlib.testing.decorators.image_comparison(
                baseline_images=baseline_images,
                extensions=["png"],
                style="mpl20",
                tol=tolerance,
            )(f),
        )

    return _decorator if f is None else _decorator(f)

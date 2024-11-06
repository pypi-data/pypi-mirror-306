"""Test configurations."""

import contextlib
import os
import shutil
from collections.abc import Callable, Generator
from unittest import mock

import pytest
from matplotlib.testing.decorators import _ImageComparisonBase  # type: ignore[attr-defined]


def _configure_save() -> contextlib.AbstractContextManager[object]:  # pragma: no cover
    orig: Callable[..., object] = _ImageComparisonBase.compare

    def compare(
        self: _ImageComparisonBase,
        fig: object,
        baseline: str,
        extension: str,
        **kwargs: object,
    ) -> object:
        try:
            return orig(self, fig, baseline, extension, **kwargs)
        except OSError:
            pass

        actual_path = (self.result_dir / baseline).with_suffix(f".{extension}")
        baseline_path = self.baseline_dir / baseline
        orig_expected_path = baseline_path.with_suffix(f".{extension}")
        orig_expected_path.parent.mkdir(exist_ok=True, parents=True)
        shutil.copy2(actual_path, orig_expected_path)
        return None

    return mock.patch.object(_ImageComparisonBase, "compare", new=compare)


@pytest.fixture(scope="session", autouse=True)
def _configure_save_fixt() -> Generator[None]:
    with (
        _configure_save()
        if os.environ.get("FAIRGROUND_RE_RECORD_MATPLOTLIB", False)
        else contextlib.nullcontext()
    ):
        yield

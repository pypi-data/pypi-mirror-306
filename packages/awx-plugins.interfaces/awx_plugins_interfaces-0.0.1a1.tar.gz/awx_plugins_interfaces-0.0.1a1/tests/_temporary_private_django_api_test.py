"""Tests for the temporarily hosted private helpers."""

from collections.abc import Callable

import pytest
from hypothesis import example, given, strategies as st

from awx_plugins.interfaces._temporary_private_django_api import (
    get_vmware_certificate_validation_setting,
    gettext_lazy,
    gettext_noop,
)


def test_vmware_cert_validation_toggle_stub() -> None:
    """Ensure the function stub returns enabled value."""
    assert get_vmware_certificate_validation_setting() is True


@example(text_input='криївка')
@example(text_input='Sich')
@given(text_input=st.text())
@pytest.mark.parametrize('invoke_gettext', (gettext_noop, gettext_lazy))
def test_gettext_functions_returns_input(
        invoke_gettext: Callable[[str], str],
        text_input: str,
) -> None:
    """Ensure ``gettext`` helpers return the input string."""
    assert text_input is invoke_gettext(text_input)

"""Tests for the temporarily hosted private helpers."""

import pathlib

import pytest

from awx_plugins.interfaces._temporary_private_licensing_api import (
    detect_server_product_name,
)


detect_server_product_name_no_cache = detect_server_product_name.__wrapped__


@pytest.mark.parametrize(
    ('path_exists', 'expected_license_name'),
    (
        pytest.param(False, 'AWX', id='AWX'),  # noqa: WPS425
        pytest.param(
            True,  # noqa: WPS425
            'Red Hat Ansible Automation Platform',
            id='AAP',
        ),
    ),
)
def test_server_product_name_detection(
        path_exists: bool,
        expected_license_name: str,
        monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Check the product detection is sound."""
    with monkeypatch.context() as mp_ctx:
        mp_ctx.setattr(pathlib.Path, 'exists', lambda _slf: path_exists)
        assert expected_license_name == detect_server_product_name_no_cache()

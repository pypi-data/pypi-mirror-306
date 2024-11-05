"""Tests for the temporarily hosted private helpers."""

from awx_plugins.interfaces._temporary_private_api import ManagedCredentialType


def test_managed_credential_type_instantiation() -> None:
    """Check that managed credential type can be instantiated."""
    assert ManagedCredentialType('', '', '', {})

"""Tests for the temporarily hosted private helpers."""

import os
import pathlib
from collections.abc import Callable

import pytest

from awx_plugins.interfaces._temporary_private_container_api import (
    CONTAINER_ROOT,
    get_incontainer_path,
)


PathOrStringType = os.PathLike[str] | str
PathToTypeCallableType = Callable[[PathOrStringType], PathOrStringType]


@pytest.mark.parametrize(
    ('host_path', 'host_runner_path', 'expected_incontainer_path'),
    (
        ('/root', '/', f'{CONTAINER_ROOT}/root'),
        ('/tmp/private/subdir', '/tmp/private', f'{CONTAINER_ROOT}/subdir'),
    ),
)
@pytest.mark.parametrize('convert_path_to_type', (pathlib.Path, str))
@pytest.mark.parametrize('convert_runner_path_to_type', (pathlib.Path, str))
def test_host_to_incontainer_path_conversion(
        host_path: os.PathLike[str] | str,
        host_runner_path: os.PathLike[str] | str,
        expected_incontainer_path: str,
        convert_path_to_type: PathToTypeCallableType,
        convert_runner_path_to_type: PathToTypeCallableType,
) -> None:
    """Ensure the positive case path conversion works."""
    typed_host_path = convert_path_to_type(host_path)
    typed_host_runner_path = convert_runner_path_to_type(host_runner_path)

    incontainer_path = get_incontainer_path(
        typed_host_path,
        typed_host_runner_path,
    )
    assert expected_incontainer_path == incontainer_path


@pytest.mark.parametrize('host_runner_path', ('', 'somewhere/'))
@pytest.mark.parametrize('convert_runner_path_to_type', (pathlib.Path, str))
def test_relative_private_data_path_conversion(
        host_runner_path: os.PathLike[str] | str,
        convert_runner_path_to_type: PathToTypeCallableType,
) -> None:
    """Ensure relative data paths are rejected."""
    typed_host_runner_path = convert_runner_path_to_type(host_runner_path)

    err_msg_pattern = '^The private_data_dir path must be absolute$'
    with pytest.raises(RuntimeError, match=err_msg_pattern):
        get_incontainer_path('', typed_host_runner_path)


@pytest.mark.parametrize(
    ('host_path', 'host_runner_path'),
    (
        ('/root', '/home'),
        ('/tmp/public/subdir', '/tmp/private'),
    ),
)
@pytest.mark.parametrize('convert_path_to_type', (pathlib.Path, str))
@pytest.mark.parametrize('convert_runner_path_to_type', (pathlib.Path, str))
def test_paths_outside_private_path_conversion(
        host_path: os.PathLike[str] | str,
        host_runner_path: os.PathLike[str] | str,
        convert_path_to_type: PathToTypeCallableType,
        convert_runner_path_to_type: PathToTypeCallableType,
) -> None:
    """Ensure paths external to private data path are rejected."""
    resolved_host_path = pathlib.Path(host_path).resolve()
    resolved_host_runner_path = pathlib.Path(host_runner_path).resolve()

    typed_host_path = convert_path_to_type(host_path)
    typed_host_runner_path = convert_runner_path_to_type(host_runner_path)

    err_msg_pattern = (
        f'^Cannot convert path {resolved_host_path !s} unless it is '
        f'a subdir of {resolved_host_runner_path !s}$'
    )
    with pytest.raises(RuntimeError, match=err_msg_pattern) as raised_exc_info:
        get_incontainer_path(typed_host_path, typed_host_runner_path)

    assert isinstance(raised_exc_info.value.__cause__, ValueError)
